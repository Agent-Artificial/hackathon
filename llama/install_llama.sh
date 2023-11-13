#! /bin/bash

#!/bin/bash

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

bash example.sh