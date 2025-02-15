import json
import requests

def chat_with_model():
    stream = True
    url = "https://proxy.tune.app/chat/completions"
    headers = {
        "Authorization": "sk-tune-6Qdfq8Zs7FYPTasaDaES2Y0kM2SZldwVTHc", #api key tvoi suda
        "Content-Type": "application/json",
    }
    
    messages = []

    while True:
        user_input = input("Вы: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        messages.append({"role": "user", "content": user_input})

        data = {
            "temperature": 0.8,
            "messages": messages,
            "model": "openai/gpt-4o",
            "stream": stream,
            "frequency_penalty": 0,
            "max_tokens": 8192
        }

        response = requests.post(url, headers=headers, json=data, stream=True)
        
        if response.status_code == 200:
            print("Модель: ", end="", flush=True)
            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith("data: "):
                        chunk = line[6:]
                        if chunk != "[DONE]":
                            chunk_json = json.loads(chunk)
                            content = chunk_json['choices'][0]['delta'].get('content', '')
                            print(content, end="", flush=True)
            print()
            messages.append({"role": "assistant", "content": content})
        else:
            print(f"Ошибка: {response.status_code}")
            print(response.text)

if __name__ == "__main__":
    chat_with_model()
