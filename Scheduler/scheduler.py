import os
import json
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from datetime import datetime, timedelta
import time
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from a `.env` file
load_dotenv()
client = OpenAI()
class SchedulerThread:
    def __init__(self, schedule_file, daily_care_file, message_callback=None):
        self.schedule_file = schedule_file
        self.scheduler = BackgroundScheduler()
        self.running = True
        self.daily_care = daily_care_file
        self.message_callback = message_callback

    def load_schedule(self):
        """
        Load the JSON schedule from the file.
        """
        with open(self.schedule_file, "r") as file:
            return json.load(file)
    
    def load_daily_care(self):
        """
        Load the JSON daily_care from the file.
        """
        with open(self.daily_care, "r") as file:
            return json.load(file)
    
    def execute_activity_with_callback(self, activity):
        """
        Wrapper for execute_activity that handles the callback
        """
        reminder_msg = self.execute_activity(activity)
        if reminder_msg and reminder_msg != "None" and reminder_msg != "none":
            if self.message_callback:
                self.message_callback(reminder_msg)
    def gpt_generate_description(self, activity):
        """
        Generate a natural language description for an activity using GPT-4.
        """

        prompt = f"Provide activity reminder and description for the following activity:\n\n{json.dumps(activity, indent=4)}"
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a caregiver for alzheimer's patients that formats JSON activity descriptions into natural language to remind the patient."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"gpt_generate_description Error generating description: {e}"
    def agent_med_activity(self, activity, past_medications):
        system_message = """The medication past event are all the event has been done, the schedule event is proposed event might need to be reminded. 
First: Find the current time within the schedule event.
Second: Create a time region where time is [current time - 2 hour, current time]
Third: If in the past medication event, there is medicine fall within this time region ( [current time - 2 hour, current time], more than 2 hours prior can not be considered as taken). Then  consider this medicine to be taken for this medication name in the schedule event.
Fourth: Recheck if the passed event time is in the region again.
 If there is medicine not taken in the past event please output a reminder for the patient to take that medicine.  And the reminder part only involve the medication name and dosage and taking time. 
Follow this output  format Reminder: "Please take your "med name" "num "pill and "med name" "num" pill at"time  "
 If there schedule events have already been done, please return None. """
        content = f"""
        passed event: {json.dumps(past_medications, indent=4)}
        schedule event: {json.dumps(activity, indent=4)}
        """
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": content}
                ]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"agent_med_activity Error generating description: {e}"
    def agent_therapy_activity(self,activity,past_therapies):
        
        content = f"""
        passed event: {json.dumps(activity, indent=4)}
        schedule event: {json.dumps(past_therapies, indent=4)}
        """
        system_message = "Past event means the therapy has been done, if the scheduled event has the same one in the past event and the past event has time list not empty, Then return None (with not punctuation or space) else you can return a reminder in natural language for this event."
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": content}
                ]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"gpt_generate_description Error generating description: {e}"
    def final_reminder_medication_output(self,intermediate_result):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Please extract reminder sentences out of the content provided and rewrite the reminder to proper grammarly correct friendly sentences with punctuation for the patient and do not forget dosage and time in the reminder. If the final result is None. Return None again without any punctuation or space. These are all restricted requirements."},
                    {"role": "user", "content": intermediate_result}
                ]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"gpt_generate_description Error generating description: {e}"
    def execute_activity(self, activity):
        """
        Execute the scheduled activity and handle it based on its type.
        """
        # Load the daily care data
        daily_care = self.load_daily_care()

        # Determine the type of the activity
        activity_type = activity.get("type")

        if activity_type == "Medication":
            # Extract medication information from daily care and call the medication agent function
            past_medications = daily_care.get("medication", [])
            intermediate_result = self.agent_med_activity(activity, past_medications)
            print(intermediate_result)
            final_output = self.final_reminder_medication_output(intermediate_result)
            if final_output == "None" or final_output == "none":
                print("None is returned")
                return None
            else:
                print("FINAL OUTPUT: " + final_output)
                return final_output
        elif activity_type == "Therapy":
            # Extract therapy information from daily care and call the therapy agent function
            past_therapies = daily_care.get("Therapy", [])
            therapy_output= self.agent_therapy_activity(activity, past_therapies)
            print(therapy_output)
            return therapy_output
        else:
            # Default handling: generate a description and log it
            description = self.gpt_generate_description(activity)
            return description

    
    def schedule_activities(self):
        """
        Load tasks from the schedule file and add them to the scheduler.
        """
        schedule_data = self.load_schedule()
        today = datetime.today().strftime("%Y-%m-%d")
        self.scheduler.remove_all_jobs()  # Clear existing jobs

        for day_schedule in schedule_data["Schedule"]:
            if day_schedule["date"] == today:  # Match today's date
                for activity in day_schedule["activities"]:
                    activity_time = datetime.strptime(activity["time"], "%H:%M").time()
                    schedule_time = datetime.combine(datetime.today(), activity_time)
                    now = datetime.now()

                    if schedule_time > now:  # Only schedule future tasks
                        print(f"Scheduling: {activity['details']} at {schedule_time}")
                        trigger = DateTrigger(run_date=schedule_time)
                        self.scheduler.add_job(
                            self.execute_activity_with_callback, 
                            trigger, 
                            args=[activity]
                        )
    def run_scheduler(self):
        """
        Start the scheduler and run it in a loop.
        """
        self.scheduler.start()
        self.schedule_activities()

        print("Scheduler is running. Press Ctrl+C to stop.")
        # If the main program is already keep running, no need for this. This is just to kee the thread alive.
        # Or we need extra logic here.
        # try:
        #     while self.running:
        #         time.sleep(1)  # Keep the thread alive
        # except KeyboardInterrupt:
        #     print("Stopping scheduler...")
        #     self.scheduler.shutdown()

    def stop(self):
        """
        Stop the scheduler gracefully.
        """
        self.running = False
        self.scheduler.shutdown()

# Exportable function for external use
def create_scheduler(schedule_file, daily_care_file, message_callback=None):
    return SchedulerThread(schedule_file, daily_care_file, message_callback)