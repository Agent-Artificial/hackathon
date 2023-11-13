import subprocess
import os
from pathlib import Path

from loguru import logger

install_llama_sh = """#!/bin/bash

# Update apt
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3.10 python3-pip build-essential libssl-dev libffi-dev python3-dev python3-venv python3-setuptools wget curl libgl1-mesa-glx libglib2.0-0 libsm6 libxext6 libxrender-dev libxslt1.1 libxslt1-dev libxml2 libxml2-dev python-is-python3 libpugixml-dev libtbb-dev git git-lfs ffmpeg libclblast-dev cmake make

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Update pip
python -m pip install --upgrade pip
pip install setuptools wheel

# Install CUDA
pip install nvidia-pyindex
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-ubuntu2204.pin
sudo mv cuda-ubuntu2204.pin /etc/apt/preferences.d/cuda-repository-pin-600
wget https://developer.download.nvidia.com/compute/cuda/12.3.0/local_installers/cuda-repo-ubuntu2204-12-3-local_12.3.0-545.23.06-1_amd64.deb
sudo dpkg -i cuda-repo-ubuntu2204-12-3-local_12.3.0-545.23.06-1_amd64.deb
sudo cp /var/cuda-repo-ubuntu2204-12-3-local/cuda-*-keyring.gpg /usr/share/keyrings/
sudo apt-get update
sudo apt-get -y install cuda-toolkit-12-3

# Install Llama.cpp
git clone https://github.com/ggerganov/llama.cpp.git
cd llama.cpp
make clean
make

# Download model
wget https://huggingface.co/TheBloke/dolphin-2.2.1-mistral-7B-GGUF/resolve/main/dolphin-2.2.1-mistral-7b.Q5_K_M.gguf -o models/mistral-dolphin-7b.gguf

mkdir -p in

bash example.sh
"""
run_llama_py = """import subprocess
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
        logger.exception(f"Subprocess failed with error:\\n{error}")
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
"""
example_sh = """#! /bin/bash

python run_llama.py
"""
system_prompt_txt = """System: 
You are a friendly and helpful chat bot

Llama: 
Hi there how are you today?

User:
I am great, how are you?

Llama:

Doing great, what can I help you with today?

User:"""

paths = {
    "install_llama_sh": "install_llama.sh",
    "run_llama_py": "run_llama.py",
    "example_sh": "example.sh",
    "system_prompt_txt": "in/system_prompt.txt",
}
data = {
    "install_llama_sh":install_llama_sh,
    "run_llama_py":run_llama_py,
    "example_sh":example_sh,
    "system_prompt_txt":system_prompt_txt,
}

path = Path

os.mkdir("in")


def write_file(file_data: str, file_path: str) -> None:
    logger.debug(f"\\nfile_data: {file_data}\\nfile_path: {file_path}\\n")
    save_path = path.cwd() / file_path
    save_path.write_text(file_data)
    save_path.chmod(0o777)


for file, pat in paths.items():
    write_file(data[file], paths[file])
    logger.debug(f"\\nfile: {file}\\n")

subprocess.run(["bash", "install_whisper.sh"], check=True)
