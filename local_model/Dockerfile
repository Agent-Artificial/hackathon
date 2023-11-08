FROM ollama/ollama as ollama

RUN echo "auto installing mistral"

# auto install ollama/mistral
RUN ollama serve & sleep 2 && ollama pull mistral

RUN echo "installing litellm"

RUN apt-get update

# Install Python
RUN apt-get install -y python3 python3-pip

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt

RUN python3 -m pip install litellm
COPY start.sh /start.sh
ENTRYPOINT [ "/bin/bash", "/start.sh" ]
