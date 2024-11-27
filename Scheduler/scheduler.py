import os
import json
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from datetime import datetime
import time
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from a `.env` file
load_dotenv()
client = OpenAI()
class SchedulerThread:
    def __init__(self, schedule_file):
        self.schedule_file = schedule_file
        self.scheduler = BackgroundScheduler()
        self.running = True

    def load_schedule(self):
        """
        Load the JSON schedule from the file.
        """
        with open(self.schedule_file, "r") as file:
            return json.load(file)

    def gpt_generate_description(self, activity):
        """
        Generate a natural language description for an activity using GPT-4.
        """
        prompt = f"Create a natural language description for the following activity:\n\n{json.dumps(activity, indent=4)}"
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
            return f"Error generating description: {e}"

    def execute_activity(self, activity):
        """
        Execute the scheduled activity and print a natural language description.
        """
        description = self.gpt_generate_description(activity)
        print(f"[{datetime.now()}]{description}")

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
                        self.scheduler.add_job(self.execute_activity, trigger, args=[activity])

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
def create_scheduler(schedule_file):
    return SchedulerThread(schedule_file)