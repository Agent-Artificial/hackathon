from autogen import oai
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

local_model_url = os.getenv("local_model_url")
if (local_model_url): print("local model: ", local_model_url)

# Create the base configuration
config = {
    "model": "ollama/mistral",
    "api_type": "open_ai",
    "api_key": os.getenv("API_KEY"),  # Assumes you also have API_KEY defined in .env
}

# Conditionally add the api_base if local_model_url is not None
if local_model_url:
    config["api_base"] = local_model_url
    print("config:", config)

# Create a text completion request
response = oai.Completion.create(
    config_list=[config],
    prompt="Hi, how are you?",
)

# create a chat completion request
response = oai.ChatCompletion.create(
    config_list=[config],
    messages=[{"role": "user", "content": "Hi, how are you?"}]
)
print(response)
