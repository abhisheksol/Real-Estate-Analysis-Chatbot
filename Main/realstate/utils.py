# analysis/utils.py
import requests
import json

OPENROUTER_API_KEY = "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"

def generate_summary_from_llm(prompt):
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost",
                "X-Title": "RealEstateBot",
            },
            data=json.dumps({
                "model": "deepseek/deepseek-r1-zero:free",
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            })
        )
        response_data = response.json()
        return response_data['choices'][0]['message']['content']
    except Exception as e:
        return "LLM summary could not be generated."
