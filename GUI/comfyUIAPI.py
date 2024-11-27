import requests

class CustomAPI:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key

    def call(self, model_name, messages, max_tokens=150):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        payload = {
            "model": model_name,
            "messages": messages,
            "max_tokens": max_tokens
        }
        response = requests.post(self.base_url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            print(f"Error {response.status_code}: {response.text}")
            return None
