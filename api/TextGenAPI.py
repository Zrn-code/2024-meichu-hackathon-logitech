import os
import requests


api_key = os.getenv('OPENAI_API_KEY')

headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {api_key}"
}

def background_to_text(background_base64):
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": "Describe the environment of this image in exactly six words: two adjectives and the name of the scene."
                },
                {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{background_base64}",
                    "detail": "low"
                }
                }
            ]
            }
        ],
        "max_tokens": 300
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    response = response.json()
    response = response['choices'][0]['message']['content']
    print(response)
    return response
    
def sketch_to_text(sketch_base64):
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": "Look at the sketch and list the six most likely objects it represents, separated by commas, without using adjectives."
                },
                {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{sketch_base64}",
                    "detail": "low"
                }
                }
            ]
            }
        ],
        "max_tokens": 300
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    response = response.json()
    response = response['choices'][0]['message']['content']
    print(response)
    return response



def sketch_to_one_text(sketch_base64):
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": "Look at the sketch and respond with only the name of the object, nothing else."
                },
                {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{sketch_base64}",
                    "detail": "low"
                }
                }
            ]
            }
        ],
        "max_tokens": 300
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    response = response.json()
    response = response['choices'][0]['message']['content']
    print(response)
    return response
