import os
import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from groq import Groq

# Load environment variables
load_dotenv()

# Set API keys and Telegram credentials
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHANNEL_ID = os.getenv('TELEGRAM_CHANNEL_ID')

# Initialize the Groq client
client = Groq(api_key=GROQ_API_KEY)

# FastAPI app instance
app = FastAPI()

# Input model for the request
class BookRequest(BaseModel):
    book_name: str

def chat_template_creation(book_name):
    messages = [
        {
            "role": "system",
            "content": f"""
                    Generate a summary of the book {book_name} with the following format:
                                *Book Name* by *Author Name*

                                *Overview*
                                Provide a brief overview of the book's content and main themes.

                                *Principal Insights*
                                1. Key Insight 1
                                2. Key Insight 2
                                3. Key Insight 3
                                4. Key Insight 4
                                5. Key Insight 5
                                6. Key Insight 6
                                7. Key Insight 7

                                *Application in Practical Life*
                                - Application Point 1
                                - Application Point 2
                                - Application Point 3
                                - Application Point 4
                                - Application Point 5

                                *Related Readings*
                                - _Related Book 1_ and brief description
                                - _Related Book 2_ and brief description
                                - _Related Book 3_ and brief description
                                - _Related Book 4_ and brief description

                                *Final Thoughts*
                                _Provide concluding thoughts on the book_.

                                Include the formatting symbols as specified in the format. Ensure the final thoughts content starts and ends with a underscore symbol. Enusre to use a single asterisk (*) for highlighting the subheadings and other keywords instead of ##. Give the summary with specified format as a python string
                                Don't use double asterisks, use only single asterisks for highlighting the text
                                
                                """
        },
        {
            "role": "user",
            "content": f"Generate a summary of the book *{book_name}*."
        }
    ]
    return messages

def summary_generation(messages):
    chat_completion = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=messages,
        temperature=0.5,
        max_tokens=1024
    )
    return chat_completion.choices[0].message.content

def send_message(token, channel_id, message, parse_mode='Markdown'):
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {
        'chat_id': channel_id,
        'text': message,
        'parse_mode': parse_mode
    }
    response = requests.post(url, data=payload)
    return response.json()

@app.post("/generate_summary/")
async def generate_summary(book_request: BookRequest):
    book_name = book_request.book_name
    try:
        chat_template = chat_template_creation(book_name)
        summary = summary_generation(chat_template)
        tg_response = send_message(TOKEN, CHANNEL_ID, summary)
        return {"telegram_response": tg_response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
