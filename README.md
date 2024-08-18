# FastAPI Book Summary Generator

## Overview

This FastAPI application is designed to generate a detailed summary of a book using the Groq API and deliver it to a specified Telegram channel. The summary includes an overview, principal insights, practical applications, related readings, and final thoughts. The application accepts a book name as input and returns a formatted summary, which is then sent to a Telegram channel.

## Features

- **Book Summary Generation:** Generates a detailed summary of a book using the Groq API.
- **Telegram Integration:** Sends the generated summary to a specified Telegram channel.
- **Environment Variables:** Utilizes environment variables for secure storage of API keys and Telegram credentials.

## Requirements

- Python 3.7+
- FastAPI
- Groq API key
- Telegram Bot Token and Channel ID
- dotenv for environment variable management
- requests for making HTTP requests

## Installation

1. **Clone the Repository:**
   \`\`\`bash
   git clone <repository-url>
   cd <repository-directory>
   \`\`\`

2. **Create a Virtual Environment:**
   \`\`\`bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\\Scripts\\activate`
   \`\`\`

3. **Install Dependencies:**
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

4. **Set Up Environment Variables:**
   Create a `.env` file in the project root directory and add the following:
   \`\`\`plaintext
   GROQ_API_KEY=your_groq_api_key
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token
   TELEGRAM_CHANNEL_ID=your_telegram_channel_id
   \`\`\`

## Project Structure

\`\`\`
.
├── main.py                # The main FastAPI application file
├── .env                   # Environment variables file (not included in the repository)
├── requirements.txt       # Python dependencies
├── README.md              # Documentation file
└── ...
\`\`\`

## FastAPI Application

### Endpoints

#### `POST /generate_summary/`

- **Description:** Generates a summary of the specified book and sends it to a Telegram channel.
- **Request Body:**
  - `book_name`: (string) The name of the book for which the summary is to be generated.
- **Response:**
  - `telegram_response`: JSON response from the Telegram API after sending the message.

- **Example Request:**
  \`\`\`json
  {
      "book_name": "Sapiens: A Brief History of Humankind"
  }
  \`\`\`

- **Example Response:**
  \`\`\`json
  {
      "telegram_response": {
          "ok": true,
          "result": {
              "message_id": 1234,
              "chat": {
                  "id": "@yourchannel",
                  "title": "Your Channel Title",
                  "type": "channel"
              },
              "date": 1609459200,
              "text": "*Book Name* by *Author Name*\n\n*Overview*\n..."
          }
      }
  }
  \`\`\`

### Code Explanation

- **`load_dotenv()`**: Loads environment variables from the `.env` file.
  
- **`Groq(api_key=GROQ_API_KEY)`**: Initializes the Groq client with the provided API key.
  
- **`chat_template_creation(book_name)`**: Prepares the chat template with specific formatting instructions for generating the book summary.

- **`summary_generation(messages)`**: Interacts with the Groq API to generate a summary based on the provided messages.

- **`send_message(token, channel_id, message, parse_mode='Markdown')`**: Sends the generated summary to the specified Telegram channel using the Telegram Bot API.

- **`@app.post("/generate_summary/")`**: The FastAPI route handler that processes the incoming book name, generates a summary, and sends it to the Telegram channel.

## Running the Application

1. **Start the FastAPI server:**
   \`\`\`bash
   uvicorn main:app --reload
   \`\`\`
   The application will be available at `http://127.0.0.1:8000`.

2. **Testing the API:**
   You can test the API using tools like `curl`, `Postman`, or directly via the browser at `http://127.0.0.1:8000/docs` where Swagger UI is available.

   Example using `curl`:
   \`\`\`bash
   curl -X POST "http://127.0.0.1:8000/generate_summary/" -H "Content-Type: application/json" -d '{"book_name": "Sapiens: A Brief History of Humankind"}'
   \`\`\`

## Deployment

To deploy this FastAPI application, you can use platforms like Heroku, AWS, or Docker. Ensure you securely manage your environment variables and update your Telegram Bot Token and Groq API Key accordingly.

## Contributing

If you want to contribute to this project, feel free to open issues or submit pull requests. Please ensure your code follows best practices and is well-documented.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Contact

For any inquiries or support, please contact `your-email@example.com`.

---

This documentation should help you understand the project structure, setup, and functionality of the FastAPI application for generating book summaries.
"""