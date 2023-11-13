import subprocess
from pathlib import Path

from loguru import logger

install_whisper_sh = """#!/bin/bash

# Update apt
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3.10 python3-pip build-essential libssl-dev libffi-dev python3-dev python3-venv python3-setuptools wget curl libgl1-mesa-glx libglib2.0-0 libsm6 libxext6 libxrender-dev libxslt1.1 libxslt1-dev libxml2 libxml2-dev python-is-python3 libpugixml-dev libtbb-dev git git-lfs ffmpeg libclblast-dev cmake make

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Update pip
python -m pip install --upgrade pip
pip install wheel setuptools

# Install CUDA
pip install nvidia-pyindex
#wget https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/cuda-wsl-ubuntu.pin
#sudo mv cuda-wsl-ubuntu.pin /etc/apt/preferences.d/cuda-repository-pin-600
#wget https://developer.download.nvidia.com/compute/cuda/12.3.0/local_installers/cuda-repo-wsl-ubuntu-12-3-local_12.3.0-1_amd64.deb
#sudo dpkg -i cuda-repo-wsl-ubuntu-12-3-local_12.3.0-1_amd64.deb
#sudo cp /var/cuda-repo-wsl-ubuntu-12-3-local/cuda-*-keyring.gpg /usr/share/keyrings/
#sudo apt-get update
#sudo apt-get -y install cuda-toolkit-12-3

# Install whisper.cpp
git clone https://github.com/ggerganov/whisper.cpp.git
cd whisper.cpp
make clean
WHISPER_CBLAST=1 make -j

# Download Whisper model
bash models/download-ggml-model.sh base.en
    
# Make in and out dirs
cd .. 
mkdir -p in out

# Run example
bash example.sh
"""
example_sh = """#! /bin/bash

cp whisper.cpp/samples/jfk.wav in

python convert_file.py in/jfk.wav

python whisper.py -f in/jfk.wav -m whisper.cpp/models/ggml-base.en.bin -o out -w whisper.cpp/main
"""

convert_file_py = """import argparse
import subprocess
from pathlib import Path

path = Path


def convert_to_wav(file_path):
    input_name = path.absolute(file_path)
    output_name = input_name.name.format("wav")
    output_path = path.cwd() / "out" / output_name
    subprocess.run(
        [
            "ffmpeg",
            "-i",
            f"{input_name}",
            "-ar",
            "16000",
            "-ac",
            "1",
            "-c:a",
            "pcm_s16le",
            f"{output_path}",
        ],
        check=True,
    )


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file_path", type=str, required=True)
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    file_path = parse_args().file_path
    convert_to_wav(file_path)
"""

whisper_py = """import argparse
import subprocess
from pathlib import Path

from loguru import logger

path = Path


def run_whisper(
    whisper_bin="whisper.cpp/main",
    file_path="in/jfk.wav",
    model_path="whisper.cpp/models/ggml-base.en.bin",
):
    file_path = path.cwd() / file_path
    model_path = path.cwd() / model_path
    try:
        result = subprocess.run(
            [f"{whisper_bin}", "-m", f"{model_path}", "-f", f"{file_path}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        logger.debug(result.stdout.decode("utf-8"))
        return result.stdout.decode("utf-8")
    except subprocess.CalledProcessError as error:
        logger.error(error)
        return error
    except RuntimeError as error:
        logger.error(error)
        return error


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f", "--file_path", default="input/jfk.wav", type=str, required=False
    )
    parser.add_argument(
        "-m",
        "--model_path",
        default="whisper.cpp/models/ggml-base.en.bin",
        type=str,
        required=False,
    )
    parser.add_argument("-w", "--whisper_bin", default="whisper.cpp/main", type=str)
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()
    run_whisper(**vars(args))
"""

paths = {
    "install_whisper_sh": "install_whisper.sh",
    "example_sh": "example.sh",
    "convert_file_py": "convert_file.py",
    "whisper_py": "whisper.py",
}
data = {
    "install_whisper_sh": install_whisper_sh,
    "example_sh": example_sh,
    "convert_file_py": convert_file_py,
    "whisper_py": whisper_py,
}

path = Path


def write_file(file_data: str, file_path: str) -> None:
    logger.debug(f"\\nfile_data: {file_data}\\nfile_path: {file_path}\\n")
    save_path = path.cwd() / file_path
    save_path.write_text(file_data)
    save_path.chmod(0o777)


for file, pat in paths.items():
    write_file(data[file], paths[file])
    logger.debug(f"\\nfile: {file}\\n")

subprocess.run(["bash", "install_whisper.sh"], check=True)
