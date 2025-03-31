import requests

url = "http://10.189.26.12:30080/model/llama3-3-70B-DSR1/v1/chat/completions"
headers = {
    "apiKey": "kep9496", # your KID
    "accept": "application/json",
    "Content-Type": "application/json"
}
messages = [
{"role":"user", "content":"Hello there how are you?"},
{"role":"assistant", "content":"Good and you?"},
{"role":"user", "content":"Does this clinical impression indicate cancer progression. Categorize as progression, regression, or stable: Patient presents with [specific symptoms, e.g., weight loss, fatigue, localized pain] and recent imaging/laboratory findings indicating [e.g., new masses, increased lesion size, elevated tumor markers]. Physical examination reveals [findings such as lymphadenopathy or organomegaly]. Based on the current clinical and diagnostic findings, further evaluation is required to assess the extent of disease and adjust treatment accordingly."}]
data = {
    "model": "llama3-3-70B-DSR1", 
    "messages": messages, 
    "max_tokens": 1000,
    "temperature" : 0.4,
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
cleaned_response = assistant_response.split("</think>\n\n")[-1] if "</think>\n\n" in assistant_response else assistant_response
print(cleaned_response)
