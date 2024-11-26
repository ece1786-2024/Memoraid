import os,sys,re,math,copy, random, time,json
import argparse
import numpy as np
import pandas as pd

import asyncio
from shiny import App, ui
from utils import *

from openai import OpenAI


##### temp model settings
models = ["gpt-4o-2024-05-13", "gpt-4o-2024-08-06", "gpt-4o-2024-11-20", "gpt-4o-mini-2024-07-18"]
openai_params = {"model":models[-1],"temperature":0, "max_tokens":300, "top_p":0.5}
api_key = "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"  # Replace with your key
## Conversation log path
MAIN_CONVLOG_PATH  = "./Conv_Log/main.json"

######## web ui setup
app_ui = ui.page_fluid(
    ui.panel_title("Memoraid"),
    ui.chat_ui("chat"),
)
# welcome message
welcome = ui.markdown(
    """
    Hi, type any message to query or memorize your information.\n
    ---
    """
)

##
def server(input, output, session):
    chat = ui.Chat(id="chat", messages=[welcome])
    #
    last_interaction_time = time.time()
    ## init log
    conversations = {}  # Dictionary to store conversations
    current_conversation=initialize_conversation()
    ##
    async def save_and_clear_chat():
        nonlocal current_conversation
        if len(current_conversation)>0 and len(current_conversation['messages'])>0:
            save_conversation_history(current_conversation, MAIN_CONVLOG_PATH)
            current_conversation = initialize_conversation()
        await chat.clear_messages()
        await chat.append_message(welcome)

    # Handle user input
    @chat.on_user_submit
    async def _():
        nonlocal last_interaction_time, current_conversation
        if current_conversation['start_time']==None:
            current_conversation['start_time'] = get_time()
        # Discard the user's message
        user_message = chat.user_input()
        last_interaction_time=time.time()
        current_conversation['messages'].append({'role': 'user', 'content': user_message})

        # Generate res with base gpt model
        ###################################################
        ### change to comfy ui pipline API
        _,agent_res_msg = basic_openai_chat_completion(api_key, openai_params, current_conversation["messages"])
        await chat.append_message(agent_res_msg)
        current_conversation['messages'].append({'role': 'assistant', 'content': agent_res_msg})
        last_interaction_time=time.time()

    # Background task to send reminders for scheduled events
    async def send_good_messages():
        nonlocal last_interaction_time, current_conversation
        try:
            while True:
                ########################################
                ### Modify for scheduled events reminder 
                await asyncio.sleep(33)
                await save_and_clear_chat()
                agent_reminder_msg = "Take some vitaminC pills"
                await chat.append_message(agent_reminder_msg)
                # current_conversation=initialize_conversation()
                if current_conversation['start_time']==None:
                    current_conversation['start_time'] = get_time()
                current_conversation['messages'].append({'role': 'assistant', 'content': "Agent proactively reminded:\n"+agent_reminder_msg})
                last_interaction_time=time.time()
        except asyncio.CancelledError:
            # raise KeyboardInterrupt("error")
            pass  # Handle task cancellation gracefully
    ##
    # Background task to check for user inactivity
    async def check_inactivity():
        nonlocal last_interaction_time, current_conversation
        try:
            while True:
                await asyncio.sleep(1)  # Check every second
                current_time = time.time()
                if (len(current_conversation['messages'])>0) and (current_time - last_interaction_time > 30):
                    # Clear chat history
                    await save_and_clear_chat()#chat.clear_messages()
                    # Optionally, reset last interaction time to prevent repeated clearing
                    last_interaction_time = current_time
        except asyncio.CancelledError:
            pass  # Handle task cancellation gracefully

    # Start the background task
    task = asyncio.create_task(send_good_messages())
    task_check_inactivity = asyncio.create_task(check_inactivity())
    # Cancel the background task when the session ends
    @session.on_ended
    async def _():
        task.cancel()
        task_check_inactivity.cancel()
        try:
            await task
            await task_check_inactivity
        except asyncio.CancelledError:
            pass

app = App(app_ui, server)
