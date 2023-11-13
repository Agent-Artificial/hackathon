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

# Install ROCm
# Make the directory if it doesn't exist yet.
# This location is recommended by the distribution maintainers.
sudo mkdir --parents --mode=0755 /etc/apt/keyrings
# Download the key, convert the signing-key to a full
# keyring required by apt and store in the keyring directory
wget https://repo.radeon.com/rocm/rocm.gpg.key -O - | \
    gpg --dearmor | sudo tee /etc/apt/keyrings/rocm.gpg > /dev/null
# Kernel driver repository for jammy
sudo tee /etc/apt/sources.list.d/amdgpu.list <<'EOF'
deb [arch=amd64 signed-by=/etc/apt/keyrings/rocm.gpg] https://repo.radeon.com/amdgpu/5.7.1/ubuntu jammy main
EOF
# ROCm repository for jammy
sudo tee /etc/apt/sources.list.d/rocm.list <<'EOF'
deb [arch=amd64 signed-by=/etc/apt/keyrings/rocm.gpg] https://repo.radeon.com/rocm/apt/debian jammy main
EOF
# Prefer packages from the rocm repository over system packages
echo -e 'Package: *\nPin: release o=repo.radeon.com\nPin-Priority: 600' | sudo tee /etc/apt/preferences.d/rocm-pin-600    
sudo apt update
sudo apt install amdgpu-dkms
sudo apt install rocm-hip-libraries


# Install Llama.cpp
git clone https://github.com/ggerganov/llama.cpp.git
cd llama.cpp
make clean
make LLAMA_HIPBLAS=1

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
