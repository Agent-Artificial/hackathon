import openai
import json

api_base = f"http://litellm:8000"

openai.api_base = api_base
openai.api_key = "temp-key"
print(openai.api_base)


print(f'LiteLLM: response from proxy with streaming')
response = openai.ChatCompletion.create(
    model="ollama/mistral", 
    messages = [
        {
            "role": "user",
            "content": "this is a test request, acknowledge that you got it"
        }
    ],
    stream=True
)

for chunk in response:
    chunk_dict = chunk.to_dict()
    content = chunk_dict["choices"][0]["delta"]["content"]
    print(f'{content}', end='')

print("\n")