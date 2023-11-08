# Use the specified base image
FROM lscr.io/linuxserver/code-server:latest

# Install nano, python3, and pip
RUN apt-get update && \
    apt-get install -y nano python3 python-is-python3 python3-pip iputils-ping git git-lfs

# Copy the contents of the local directory "../" to the /workspace directory in the container
#COPY ../ /workspace

### For Docker in Docker ###
# Install prerequisites
RUN apt-get update && apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common

# Add the Docker repository to APT sources
RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add - \
    && add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

# Install Docker
RUN apt-get update && apt-get install -y docker-ce docker-ce-cli containerd.io


# Clean up
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# 50/50 on removing this.
RUN apt-get update

# Set the working directory to /workspace
WORKDIR /workspace
