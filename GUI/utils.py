import os,sys,re,math,copy, random, time,json
import argparse
import numpy as np
import pandas as pd

from openai import OpenAI


def basic_openai_chat_completion(api_key, openai_params, conv_prompt):
    client = OpenAI(api_key=api_key)
    openai_params.update({"messages":conv_prompt})
    response = client.chat.completions.create(**openai_params)
    answer_msg = response.choices[0].message.content
    #
    return response, answer_msg




# get time
def get_time()->str:
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
# conversation log
def save_conversation_history(conv_log:dict, main_conv_log_path:str)->None:
    curr_time = get_time()
    conv_log['end_time'] = curr_time
    try:
        with open(main_conv_log_path, "r") as file:
            history = json.load(file)
    except FileNotFoundError:
        history = {}  # If the file doesn't exist, start with an empty history
    # Add the new conversation to the history
    history[curr_time] = conv_log
    # Save the updated history back to the JSON file
    with open(main_conv_log_path, "w") as file:
        json.dump(history, file, indent=4)
    # conv_log = initialize_conversation()

def initialize_conversation()->dict:
    # current_conversation_start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    return {
        'start_time': None,
        'end_time':None,
        'messages': []
    }