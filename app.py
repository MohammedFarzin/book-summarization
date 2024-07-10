# Schedule Library imported
import schedule
import time
from dotenv import load_dotenv
import os
from groq import Groq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
print(GROQ_API_KEY)

client = Groq(api_key=GROQ_API_KEY)

# List of books and authors
book_names = ["Atomic Habits", "Magic of Thinking Big", "Think and Grow Rich", "The Secret", "The Psychology of Money", "Ikigai"]
authors = ["James Clear", "David Schwartz", "Napoleon Hill", "Rhonda Byrne", "Morgan Housel", "Héctor García and Francesc Miralles"]

# List to store generated summaries
summary_generated = []

# Function to create chat template for each book
def chat_template_creation(book_names, authors):
    chat_template = []

    
    books_with_authors = dict(zip(book_names, authors))
    print(books_with_authors)

    for book_name, author in books_with_authors.items():
        messages=[
            {
                "role": "system",
                "content": f"""
                        Generate a summary of the book The {book_name} by {author}, focusing on the first two chapters. The summary should include the following:
                        - 5 Core Concepts: Briefly describe the five main ideas presented in the book.
                        - Breakthrough Ideas: Identify three key strategies or techniques introduced in the book.
                        - Quotable Insight: Include a memorable or impactful quote from the book.
                        - Practical Applications: List four specific actions or steps that readers can take based on the ideas presented in the book.
                        - Why It's a Must-Read: Explain why the book is valuable and worth reading.
                        - For Readers Who Enjoyed: Recommend two other books that readers who enjoyed The {book_name} might also enjoy.
                        - Final Thought: Summarize the overall message or theme of the book in a concise and impactful way.
                        The summary should be written in a clear and concise style, using bullet points for easy readability. It should accurately reflect the content and ideas presented in the book, and should provide readers with a useful and informative overview of the book's main points.
                """
            },
            {
                "role":"user",
                "content": f"Generate a summary of the book The {book_name} by {author}, focusing on the first two chapters."
            }
        ]

        chat_template.append(messages)
    return chat_template

# Function to generate summary for each book
def summary_generation(message):
    print("summary_generation:", message[0].get("content"))
    chat_completion = client.chat.completions.create(
    model="mixtral-8x7b-32768",
    messages=message,
    temperature=0.5,
    max_tokens=1024
    )
    print(chat_completion.choices[0].message.content)

    return chat_completion.choices[0].message.content

    

# Wrapper function to pass message to summary_generation function
def wrapper_function(message):
    print("wrapper_function", message[0].get("content"))
    summary = summary_generation(message)
    summary_generated.append(summary)


# Create chat template for each book
chat_template = chat_template_creation(book_names, authors)
current_index = 0 # Global iterator
for message in chat_template: 
    print(message[0].get("content"))
    schedule.every(5).seconds.do(wrapper_function, message)
  
# Run the schedule
while True:
    schedule.run_pending()
    time.sleep(1)
    if len(summary_generated) == len(chat_template):
        print("All summaries generated")
        print(summary_generated)
        for i in range(len(summary_generated)):
            with open(f"summary/summary_{book_names[i]}.txt", "w", encoding="utf-8") as file:
                file.write(summary_generated[i])
        break  
    
    
