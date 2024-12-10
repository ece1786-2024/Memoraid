# Scheduler Package Documentation
## All work here is done by Yilin Hui individually.

## Overview
This package implements the proactive reminder function of project Memoraid. It uses APScheduler (Advanced Python Scheduler) for handling scheduled tasks and OpenAI's GPT models for generating natural language reminders.

## Dependencies
- `apscheduler`: Used for background task scheduling
- `openai`: OpenAI API client for GPT model interactions
- `python-dotenv`: For environment variable management
- Other standard Python libraries: `os`, `json`, `datetime`, `time`

## Key Components

### SchedulerThread Class
The main class that handles all scheduling operations. It manages:
- Loading schedule data from JSON files
- Scheduling activities
- Executing activities based on their type
- Generating reminders using GPT models

## Agent Prompts

### 1. General Activity Description Agent
**Purpose**: Converts JSON activity data into natural language descriptions
**Model**: gpt-4o-mini
**System Prompt**:
```
Your job is to transfer json to a natural language sentence to remind people.
```

### 2. Medication Activity Agent
**Purpose**: Processes medication schedules and generates appropriate reminders
**Model**: gpt-4o-mini
**System Prompt**:
```
The medication past event are all the event has been done, the schedule event is proposed event might need to be reminded. 
First: Find the current time within the schedule event.
Second: Create a time region where time is [current time - 2 hour, current time]
Third: If in the past medication event, there is medicine fall within this time region ([current time - 2 hour, current time], more than 2 hours prior can not be considered as taken). Then consider this medicine to be taken for this medication name in the schedule event.
Fourth: Recheck if the passed event time is in the region again.
If there is medicine not taken in the past event please output a reminder for the patient to take that medicine. And the reminder part only involve the medication name and dosage and taking time. 
Follow this output format Reminder: "Please take your "med name" "num "pill and "med name" "num" pill at"time"
If there schedule events have already been done, please return None.
```

### 3. Therapy Activity Agent
**Purpose**: Manages therapy schedules and generates reminders
**Model**: gpt-4o-mini
**System Prompt**:
```
Past event means the therapy has been done, if the scheduled event has the same one in the past event and the past event has time within 3 hours before the schedule event time, then return None (with not punctuation or space) else you can return a reminder in natural language for this event. Do not include reminder: at the start.
```

### 4. Final Medication Reminder Formatter
**Purpose**: Reformats medication reminders into a user-friendly format
**Model**: gpt-4o-mini
**System Prompt**:
```
Please extract reminder sentences out of the content and combine or reform the reminders into a friendly sentence and split medicines with commas and put dosage in square bracket like [1 pill]. Do not forget dosage and time in this sentence. If the final result is None. Return None again without any punctuation or space. These are all restricted requirements.
```

## File Structure
The system requires two JSON files:
1. Schedule file: Contains planned activities
2. Daily care file: Tracks completed activities

## Time Window Rules
- Medication activities: 2-hour window for checking if medication was taken
- Therapy activities: 3-hour window for checking if therapy was completed
- Other activity types are reminded directly without check for completion.

## Notes
- The scheduler only processes activities scheduled for the current day
- Only future activities are scheduled when the system starts
- All GPT interactions use the gpt-4o-mini model
- The system requires an OpenAI API key to be set in the environment variables, current solution is to use dotenv pacakge.