## Memoraid GUI

This is a **Shiny-based implementation** of our project's web app, which allows users to interact with our system in a conversational manner. The web app serves as a chat GUI and demonstrates two types of user-assistant interactions:

1. **Passive Interaction**:  The system processes the user's message by forwarding it to our pipeline. Once the pipeline generates a response, it sends the reply back to the user. Users can engage in a back-and-forth conversation with the agent, which maintains awareness of the current conversation history for contextually relevant replies.
2. **Proactive Interaction**: The system initiates a conversation by sending messages to the user.

### Deployment Instructions

To deploy this GUI in your environment, follow these steps:

1. **Install Required Packages**

   Run the following command to install the necessary dependencies:

   ```bash
   pip install -r PATH_TO_requirements.txt
   ```

2. **Start the Web App**

   Navigate to the GUI directory and start the Shiny application:

   ```bash
   cd ./GUI/
   shiny run app.py
   ```

   Once the application starts successfully, follow the address provided in the Shiny output message to interact with the system.

### Notes

- All conversations with the system are logged and stored in `./GUI/Conv_Log/main.json`.
- If a user is inactive for more than 30 seconds, the current chat session is terminated. When the user sends a new message, a new chat session begins.
- When the system triggers a proactive reminder, the current chat history is ended, and a new chat session is initiated specifically for the reminder.