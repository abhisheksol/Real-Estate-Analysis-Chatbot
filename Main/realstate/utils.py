# analysis/utils.py
import requests
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
            }),
            timeout=15  # Add timeout to prevent hanging
        )
        
        # Print response code and preview for debugging
        print(f"Response status: {response.status_code}")
        print(f"Response preview: {response.text[:200]}")
        
        response_data = response.json()
        return response_data['choices'][0]['message']['content']
    except Exception as e:
        # Print the exception details for debugging
        print(f"Error in API call: {str(e)}")
        logger.error(f"LLM API Error: {str(e)}")
        
        # Return fallback summary with error message
        return f"LLM summary could not be generated. Error: {str(e)}"
