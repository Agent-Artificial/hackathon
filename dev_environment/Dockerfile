# Use the specified base image
FROM lscr.io/linuxserver/code-server:latest

# Install nano, python3, and pip
RUN apt-get update && \
    apt-get install -y nano python3 python-is-python3 python3-pip iputils-ping git git-lfs

# Copy the contents of the local directory "../" to the /workspace directory in the container
#COPY ../ /workspace

# Set the working directory to /workspace
WORKDIR /workspace
