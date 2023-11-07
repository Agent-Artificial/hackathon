import subprocess
from pathlib import Path

from loguru import logger

install_whisper_sh = """#!/bin/bash

# Update apt
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3.10 python3-pip build-essential libssl-dev libffi-dev python3-dev python3-venv python3-setuptools wget curl libgl1-mesa-glx libglib2.0-0 libsm6 libxext6 libxrender-dev libxslt1.1 libxslt1-dev libxml2 libxml2-dev python-is-python3 libpugixml-dev libtbb-dev git git-lfg ffmpeg libclblast-dev cmake make

# Update pip
python -m pip install --upgrade pip

# Create virtual environment
python -m venv .venv
source .venv/bin/activate



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

path = Path


def run_whisper(
    whisper_bin="whisper.cpp/main",
    file_path="in/jfk.wav",
    outdir="out",
    model_path="whisper.cpp/models/ggml-base.en.bin",
):
    file_path = path.cwd() / file_path
    file_name = file_path.name
    model_path = path.cwd() / model_path
    output_path = path.cwd() / outdir / f"{file_name}.txt"
    subprocess.run(
        [
            f"{whisper_bin}",
            "-m",
            f"{model_path}",
            "-f",
            f"{file_path}",
            "-otxt",
            f"{output_path}",
        ],
        check=True,
    )


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f", "--file_path", default="input/jfk.wav", type=str, required=True
    )
    parser.add_argument(
        "-m",
        "--model_path",
        default="whisper.cpp/models/ggml-base.en.bin",
        type=str,
        required=True,
    )
    parser.add_argument("-w", "--whisper_bin", default="whisper.cpp/main", type=str)
    parser.add_argument("-o", "--outdir", type=str, required=True)
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
