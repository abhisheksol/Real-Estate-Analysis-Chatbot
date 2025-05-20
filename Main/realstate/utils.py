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
