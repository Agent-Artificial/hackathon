ARG UBUNTU_VERSION=22.04

# This needs to generally match the container host's environment.
ARG CUDA_VERSION=11.7.1

# Target the CUDA build image
ARG BASE_CUDA_DEV_CONTAINER=nvidia/cuda:${CUDA_VERSION}-devel-ubuntu${UBUNTU_VERSION}

FROM ${BASE_CUDA_DEV_CONTAINER} as build

# Unless otherwise specified, we make a fat build.
ARG CUDA_DOCKER_ARCH=all

RUN apt-get update && \
    apt-get install -y build-essential git cmake python3.10 python3-pip libssl-dev libffi-dev python3-dev python3-venv python3-setuptools wget curl libgl1-mesa-glx libglib2.0-0 libsm6 libxext6 libxrender-dev libxslt1.1 libxslt1-dev libxml2 libxml2-dev python-is-python3 libpugixml-dev libtbb-dev git-lfs ffmpeg libclblast-dev make nano

RUN python -m pip install --upgrade pip

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

# Set nvcc architecture
ENV CUDA_DOCKER_ARCH=${CUDA_DOCKER_ARCH}
# Enable cuBLAS
ENV WHISPER_CUBLAS=1

# Install whisper.cpp
RUN git clone https://github.com/ggerganov/whisper.cpp.git

WORKDIR /app/whisper.cpp

RUN make clean && WHISPER_CBLAST=1 make -j

# Download Whisper model
RUN bash models/download-ggml-model.sh base.en

WORKDIR /app

# Make in and out dirs
RUN mkdir -p in out


CMD ["uvicorn","whisper_api:app","--host","0.0.0.0","--reload"]
