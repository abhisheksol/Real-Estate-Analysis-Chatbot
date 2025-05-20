# analysis/utils.py
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
OPENROUTER_API_KEY = os.environ["OPENROUTER_API_KEY"]  #

# OPENROUTER_API_KEY = "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"

def generate_summary_from_llm(prompt):
    try:
        print("running ")
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
            }),
            timeout=15  # Add timeout to prevent hanging
        )
        
        # Print response code and preview for debugging
        print(f"Response status: {response.status_code}")
        print(f"Response preview: {response.text[:200]}")
        
        response_data = response.json()
        print("Status code:", response_data)
        return response_data['choices'][0]['message']['content']
    except Exception as e:
        # Print the exception details for debugging
        print(f"Error in API call: {str(e)}")
        logger.error(f"LLM API Error: {str(e)}")
        
        # Return fallback summary with error message
        return f"LLM summary could not be generated. Error: {str(e)}"
