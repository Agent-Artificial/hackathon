import subprocess
import loguru
import argparse
from pathlib import Path

logger = loguru.logger

path = Path

def run_llama(
    prompt="",
    llama_bin="llama.cpp/main",
    interactive_or_prompt="prompt",
    model_path="llama.cpp/models/mistral-dolphin-7b.gguf",
    color=True,
    system_prompt="in/system_prompt.txt",
    context_window="8198",
    temp="0.2"
):
    try:
        main_call = [
            llama_bin, "-m", model_path, "--temp", temp, "-c", context_window
        ]
        if interactive_or_prompt == "interactive":
            main_call.append("--interactive-first")
        if interactive_or_prompt == "prompt":
            main_call.append("--prompt")
            main_call.append(prompt)
        if color == True:
            main_call.append("--color")
        if system_prompt:
            main_call.append("-f")
            main_call.append(system_prompt)
        resp = subprocess.run(main_call, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        logger.debug(resp.stdout)
        return resp.stdout
    except subprocess.CalledProcessError as error:
        logger.exception(f"Subprocess failed with error:\n{error}")
        if error.stdout:
            logger.error(f"stdout: {error.stdout}")
        if error.stderr:
            logger.error(f"sterr: {error.stderr}")

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--model_path", type=str, default="llama.cpp/models/mistral-dolphin-7b.gguf")
    parser.add_argument("-i", "--interactive_or_prompt", type=str, default="prompt")
    parser.add_argument("-c", "--context_window", type=str, default="8198")
    parser.add_argument("-t", "--temp", type=str, default="0.2")
    parser.add_argument("-s", "--system_prompt", type=str, default="in/system_prompt.txt")
    parser.add_argument("-p", "--prompt", type=str, default="")
    parser.add_argument("--color", type=bool, default=True)
    args = parser.parse_args()
    return args

    
if __name__ == "__main__":
    args = parse_args()
    run_llama(**args.__dict__)