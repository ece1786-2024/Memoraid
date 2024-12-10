import os,sys,re,math,copy, random, time,json
import argparse
import numpy as np
import pandas as pd

import asyncio
from shiny import App, ui
from utils import *

from openai import OpenAI
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Scheduler')))
from scheduler import create_scheduler

# two types of chat available, `baseline` interacts directly with chatgpt, `sys_api` interacts
# with our system
agent_mode = ["baseline", "sys_api"][0]
#comfyUI API call
if agent_mode == "sys_api":
    import comfyUIAPI
    comfyAPI = comfyUIAPI(base_url="http://127.0.0.1:8187/v1/chat/completions", api_key="testKey")


##### temp model settings
models = ["gpt-4o-2024-05-13", "gpt-4o-2024-08-06", "gpt-4o-2024-11-20", "gpt-4o-mini-2024-07-18"]
openai_params = {"model":models[-1],"temperature":0, "max_tokens":300, "top_p":0.5}
api_key = "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"
## Conversation log path
MAIN_CONVLOG_PATH  = "./Conv_Log/main.json"
os.makedirs(os.path.dirname(MAIN_CONVLOG_PATH), exist_ok=True)


## set up user profile path
TEST_DATA_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__),"../Test_Data"))
# database information
pers_info_json = load_json(os.path.join(TEST_DATA_ROOT, "Personal_info.json"))
serv_info_json = load_json(os.path.join(TEST_DATA_ROOT, "Service_info.json"))


### set up prompt for baseline model
sys_prompt = f"""
You are a helpful assistant. You task is to effectively communicate with an Alzheimer's patient (user), answering user's questions with given context.

The following are provided context regarding the user:
Pseronal information regarding the user:
{json.dumps(pers_info_json)}
Service information provided by the care provider:
{json.dumps(serv_info_json)}

Answer the following question:
"""
sys_msg = format_msg_role("system", sys_prompt)


# chat type by agent mode
def basic_chat_completion(api_key, openai_params, conv_prompt, agent_mode):
    if agent_mode == "sys_api":
        agent_res_msg = comfyAPI.call(
                model_name="original_api",
                messages=conv_prompt,
                max_tokens=150,
            )
    elif agent_mode == "baseline":
         temp_conv_prompt = [sys_msg] + conv_prompt
         _,agent_res_msg = basic_openai_chat_completion(api_key, openai_params, temp_conv_prompt)
    return agent_res_msg


#
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
    # Create an async queue for messages
    message_queue = asyncio.Queue()
    # Create an event loop for the callback
    loop = asyncio.get_event_loop()
    async def handle_reminder_message(message):
        """
        Async function to handle incoming reminder messages
        """
        await message_queue.put(message)
    def callback_bridge(msg):
        """
        Bridge function to safely handle callbacks from the scheduler thread
        """
        asyncio.run_coroutine_threadsafe(handle_reminder_message(msg), loop)
    scheduler = create_scheduler(
    "../Test_Data/schedule.json", 
    "../Test_Data/daily_care.json",
    callback_bridge
    )
    
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
        ### changed to comfy ui pipline API
        # _,agent_res_msg = basic_openai_chat_completion(api_key, openai_params, current_conversation["messages"])
        # agent_res_msg = comfyAPI.call(
        #     model_name="original_api",
        #     messages=current_conversation["messages"],
        #     max_tokens=150,
        # )
        agent_res_msg = basic_chat_completion(api_key, openai_params, current_conversation["messages"], agent_mode=agent_mode)
        await chat.append_message(agent_res_msg)
        current_conversation['messages'].append({'role': 'assistant', 'content': agent_res_msg})
        last_interaction_time=time.time()

    # Background task to send reminders for scheduled events
    async def send_good_messages():
        nonlocal last_interaction_time, current_conversation
        try:
            # Start the scheduler
            scheduler.run_scheduler()
            
            while True:
                try:
                    # Wait for messages from the queue
                    reminder_msg = await message_queue.get()
                    
                    # Send to UI
                    await chat.append_message("Reminder: " + reminder_msg)
                    
                    if current_conversation['start_time'] is None:
                        current_conversation['start_time'] = get_time()
                    
                    current_conversation['messages'].append({
                        'role': 'assistant',
                        'content': f"Agent proactively reminded:\n{reminder_msg}"
                    })
                    last_interaction_time = time.time()
                    
                    # Mark the task as done
                    message_queue.task_done()
                    
                except asyncio.CancelledError:
                    break

        except asyncio.CancelledError:
            scheduler.stop()
            pass
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
if __name__ == "__main__":
    app.run()