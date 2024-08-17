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

book_names = ["Magic of Thinking Big", "Atomic Habits", "Think and Grow Rich", "The Secret", "The Psychology of Money", "Ikigai"]
authors = ["David Schwartz", "James Clear", "Napoleon Hill", "Rhonda Byrne", "Morgan Housel", "Héctor García and Francesc Miralles"]
summary_generated = []


def chat_template_creation(book_names, authors):
    chat_template = []

    
    books_with_authors = dict(zip(book_names, authors))
    books_with_authors = books_with_authors[:1]
    print(books_with_authors)

    for book_name, author in books_with_authors.items():
        messages=[
            {
                "role": "system",
                "content": f"""
                        Generate a summary of the book {book_name} by {author} with the following format:
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
                                    `Provide concluding thoughts on the book.`

                                    Include the formatting symbols as specified in the format. Ensure the final thoughts content starts and ends with a grave accent symbol. Enusre to use a single asterisk (*) for highlighting the subheadings and other keywords instead of ##. Give the summary with specified format as a python string
                                    Don't use double asterisks, use only single asterisks for highlighting the text
                                    
                                    """
            },
            {
                "role":"user",
                "content": f"Generate a summary of the book The {book_name} by {author}."
            }
        ]

        chat_template.append(messages)
    return chat_template
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

    


def wrapper_function(message):
    print("wrapper_function", message[0].get("content"))
    summary = summary_generation(message)
    summary_generated.append(summary)


chat_template = chat_template_creation(book_names, authors)
for message in chat_template: 
    print(message[0].get("content"))
    schedule.every(5).seconds.do(wrapper_function, message)
  

# while True:
#     schedule.run_pending()
#     time.sleep(1)
#     if len(summary_generated) == len(chat_template):
#         print("All summaries generated")
#         print(summary_generated)
#         for i in range(len(summary_generated)):
#             with open(f"summary/summary_{book_names[i]}.txt", "w", encoding="utf-8") as file:
#                 file.write(summary_generated[i])
#         break  
    
    
