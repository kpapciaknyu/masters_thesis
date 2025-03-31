import requests

url = "http://10.189.26.12:30080/model/llama3-3-70b-chat/v1/chat/completions"
headers = {
    "apiKey": "kep9496", # your KID
    "accept": "application/json",
    "Content-Type": "application/json"
}
messages = [
{"role":"user", "content":"Hello there how are you?"},
{"role":"assistant", "content":"Good and you?"},
{"role":"user", "content":"When was NYU Langone Hospital founded?"}]
data = {
    "model": "llama3-3-70b-chat", 
    "messages": messages, 
    "max_tokens": 200,
    "temperature": 0.3,
    "top_p": 1,
    "n": 1,
    "stream": False,
    "stop": "string",
    "frequency_penalty": 0.0
}
response = requests.post(url, headers=headers, json=data)
print(response.status_code)
print(response.json())

print("\n\n")
assistant_response = response.json()["choices"][0]["message"]["content"]
print(assistant_response)

