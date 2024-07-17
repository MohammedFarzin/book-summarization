import requests
import os
from dotenv import load_dotenv
import schedule
import time

load_dotenv()

directory = "summary"

url = "https://gate.whapi.cloud/messages/text"

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": f"Bearer {os.environ['WHAPI_CLOUD_API_KEY']}"
}


current_index = 0 
def channel_summary(file_name):
    global current_index
    filename = file_name[current_index]
    current_index += 1
    with open(f"{directory}/{filename}", "r") as file:
        summary = file.read()


    payload = {
            "typing_time": 0,
            "to": "120363314716102514@newsletter",
            "body": summary
        }

    response = requests.post(url, json=payload, headers=headers)

    print(response.text)
    
file_name = os.listdir(directory)
schedule.every(30).seconds.do(channel_summary, file_name)





# for filename in os.listdir(directory):
#     if filename.endswith(".txt"):
#         with open(f"{directory}/{filename}", "r") as file:
#             summary = file.read()

#         payload = {
#             "typing_time": 0,
#             "to": "120363314716102514@newsletter",
#             "body": summary
#         }

#         response = requests.post(url, json=payload, headers=headers)

#         print(response.text)


  
# Run the schedule
while True:
    schedule.run_pending()
    time.sleep(1)
    if current_index == len(file_name):
        break  