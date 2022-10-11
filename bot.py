import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime, timedelta
import json
import random

# This app is used to send messages to slack API from python program based on
# selected time interval and until reach the end time (stop time).
# Version : 1.0.
# Author : Sherif Essam.
# Date: Sep. 11th 2022.

# This method is used to get all compliments from JSON file.
def get_comp_list():
    f = open('data.json', 'r')
    data = json.load(f)
    temp_list = []
    for x in data['colleagues']:
        for key, v in x.items():
            if key == "comp":
                temp_list.append(v)
    return temp_list


# Main method that takes send and stop inputs to send messages at the requested
# time interval that ends by reaching the requested stop time.
def send_messages(option_send, num_send, option_stop, num_stop):
    now = datetime.now()
    diff_send = now + get_time(option_send, num_send)
    diff_stop = now + get_time(option_stop, num_stop)
    while now <= diff_stop:
        now = datetime.now()
        if diff_send <= now:
            send_message('#happy-bot-sherif', int((datetime.now() + timedelta(seconds=15)).timestamp()))
            diff_send = now + get_time(option_send, num_send)
    print("All messages are sent!")


# The function that sends a random message to slack API.
def send_message(channel, msg_date):
    notFound = True
    rdm = ''
    if len(all_msgs) == len(comp_list):
        all_msgs.clear()
    while notFound:
        temp_rdm = (random.choice(list(comp_list)))
        if check_msg(temp_rdm):
            rdm = temp_rdm
            print(rdm)
            all_msgs.append(rdm)
            notFound = False
    client.chat_scheduleMessage(channel=channel, text=rdm, post_at=msg_date)


# A switch that is used to get the needed timedelta based on option and val parameters.
def get_time(option, val):
    if option == "seconds":
        return timedelta(seconds=val)
    elif option == "minutes":
        return timedelta(minutes=val)
    elif option == "hours":
        return timedelta(hours=val)
    else:
        return timedelta(days=val)


# A function that checks if the message was previously selected or not.
def check_msg(rdm_msg):
    for msg in all_msgs:
        if msg == rdm_msg:
            return False
    return True


# Main app function.
if __name__ == "__main__":
    env_path = Path('.') / '.env'
    load_dotenv(dotenv_path=env_path)
    client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
    comp_list = get_comp_list()
    all_msgs = []
    send_messages("minutes", 10, "hours", 2)
