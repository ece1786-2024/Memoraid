# Memoraid: A Virtual Assistant for Alzheimer’s Patients
<!-- ![Chat Example](./imgs/UI_3.png) -->
<div align="center">
    <img src="./imgs/UI_3.png" alt="Chat Example" width="70%"/>
</div>

**Memoraid** is a multi-agent virtual assistant designed to support individuals in the early to mid-stages of Alzheimer’s disease.  This project seeks to leverage the semantic understanding capabilities of LLMs to address challenges faced byAlzheimer’s patients. We propose an LLM-based multi-agent system enhanced with a dynamic personal profiling database to deliver personalized and effec tive support. This system aims to provide accurate, factual answers to common questions while assisting in managing daily routines with instructions, thereby reducing the caregiving burden.

---

## Repository Overview

This section provides an overview of the key folders and files in the repository, along with their purposes and contents.

- **Supplementaries:**
    - Implementation of passive interaction as an API.
    - Contains prompts used for agents in the passive interaction system.
- **Scheduler:**
    - Implementation of proactive interaction.
    - Includes prompts used for agents in this system.
- **GUI:**
    - Shiny implementation of the chat user interface.
- **Test_Data:**
    - Contains synthetic QA datasets and corresponding user profiles.
    - Includes prompts used to generate the QA datasets.
- **eval_results:**
    - Results of the evaluation conducted on the QA datasets.

- **evaluation.ipynb:**
    - Jupyter notebook containing scripts for evaluating the system's performance.

---

## Features
- **Personalized Assistance**: Accurate responses tailored to the user’s condition.
- **Cost-effective Caregiving**: Aiming to reduce the burdon on caregiver with low cost.

---
## System structure:
Our system supports two types of patient interactions:
    – Passive: Patient initiates conversation to request information (i.e. details ofamenities of their care facility).
    – Proactive: The system proactively sends reminders based on a predefined schedule (i.e. prompting the patient to follow therapy routine)

<div align="center">
    <img src="./imgs/passive_chat.png" alt="passive interaction" width="80%"/>
</div>
<!-- ![passive interaction](imgs/passive_chat.png) -->

 *Figure 1: Passive interaction workflow.*

<div align="center">
    <img src="./imgs/reminder.png" alt="proactive interaction" width="80%"/>
</div>
<!-- ![proactive interaction](imgs/reminder.png) -->

 *Figure 2: Proactive interaction workflow.*

---

## Demo
To experience the full capabilities of **Memoraid**, follow the setup instructions for both the **GUI** and the **ComfyUI** components.

### Setup Instructions

1. **[GUI Setup](GUI/)**
   - Includes the user interface (UI) and reminder system.
   - Note: If baseline_mode is selected, ComfuUI API is not required. Refer to [Agent Mode Selection](GUI/ReadMe.md)
2. **[ComfyUI Setup](Supplementaries/)**
   - Enables passive interaction capabilities.
   

Both components must be set up correctly to access all features provided by the demo. 

---

## Acknowledgements

This project was developed as part of the **ECE1786** course. We extend our gratitude to the teaching team for providing such a wonderful and enriching learning experience.

---

