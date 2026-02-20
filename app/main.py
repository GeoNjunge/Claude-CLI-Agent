import argparse
import os
import sys
import json
import subprocess

from openai import OpenAI

API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = os.getenv("OPENROUTER_BASE_URL",
                     default="https://openrouter.ai/api/v1")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("-p", required=True)
    args = p.parse_args()

    if not API_KEY:
        raise RuntimeError("OPENROUTER_API_KEY is not set")

    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
    msgs = [{"role": "user", "content": args.p}]

    while True:
        chat = client.chat.completions.create(
            model="anthropic/claude-haiku-4.5",
            messages=msgs,
            tools=[
                {
                    "type": "function",
                    "function": {
                        "name": "Read",
                        "description": "Read and return the contents of a file",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "file_path": {
                                    "type": "string",
                                    "description": "The path to the file to read"
                                }
                            },
                            "required": ["file_path"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "Write",
                        "description": "Write content to a file",
                        "parameters": {
                            "type": "object",
                            "required": ["file_path", "content"],
                            "properties": {
                                "file_path": {
                                    "type": "string",
                                    "description": "The path of the file to write to"
                                },
                                "content": {
                                    "type": "string",
                                    "description": "The content to write to the file"
                                }
                            }
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "Bash",
                        "description": "Execute a shell command",
                        "parameters": {
                            "type": "object",
                            "required": ["command"],
                            "properties": {
                                "command": {
                                    "type": "string",
                                    "description": "The command to execute"
                                }
                            }
                        }
                    }
                }
            ]
        )

        if not chat.choices or len(chat.choices) == 0:
            raise RuntimeError("no choices in response")

        # You can use print statements as follows for debugging, they'll be visible when running tests.
        print("Logs from your program will appear here!", file=sys.stderr)

        # TODO: Uncomment the following line to pass the first stage

        msgs.append({
            "role": "assistant",
            "content": chat.choices[0].message.content,
            "tool_calls": chat.choices[0].message.tool_calls,
        })

        if chat.choices[0].message.tool_calls and len(chat.choices[0].message.tool_calls) > 0:
            for tool_call in chat.choices[0].message.tool_calls:
                function_name = tool_call.function.name
                arguments = tool_call.function.arguments

                parsed_args = json.loads(arguments)

                if function_name == "Write":
                    file_path = parsed_args["file_path"]
                    content = parsed_args["content"]
                    with open(file_path, "a") as file:
                        file.write(content)
                        msgs.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": content
                        })

                elif function_name == "Read":
                    file_path = parsed_args["file_path"]
                    with open(file_path, "r") as file:
                        content = file.read()
                        msgs.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": content
                        })

                elif function_name == "Bash":
                    command = parsed_args["command"]

                    result = subprocess.run(
                        command, capture_output=True, shell=True, text=True, cwd='.')

                    if result.returncode == 0:
                        output = result.stdout
                    else:
                        output = result.stderr

                    msgs.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": output
                    })

        else:
            print(chat.choices[0].message.content)
            msgs.append({
                "role": "assistant",
                "content": chat.choices[0].message.content,
            })
            break


if __name__ == "__main__":
    main()
