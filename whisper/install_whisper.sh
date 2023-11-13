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
