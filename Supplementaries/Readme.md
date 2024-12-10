# Memoraid Deployment Guide

## Overview

Memoraid's update and query functions are built on top of two existing GitHub projects: [ComfyUI](https://github.com/comfyanonymous/ComfyUI), which provides a visual interface for workflows, and LLM-party, which supplies nodes that simplify LLM integration.

Although it is possible to convert the project to use raw Python libraries, this would require additional time to understand the underlying workings of ComfyUI and LLM-party, as well as to reconstruct the current architecture. ComfyUI's transparency and simplicity make it the best choice for our current implementation.

## Setup Instructions

### Prerequisites
1. Download ComfyUI and ComfyUI Manager.
2. Install comfyui_LLM_party using ComfyUI Manager.

### Step-by-Step Setup
1. **Download ComfyUI**: [GitHub Link](https://github.com/comfyanonymous/ComfyUI). Unzip the `.7z` file and navigate to `~\ComfyUI\custom_nodes`.
2. **Clone ComfyUI Manager**: Run the following in terminal:
   ```sh
   git clone https://github.com/ltdrdata/ComfyUI-Manager.git
   ```
3. **Launch ComfyUI**: Run `run_nvidia_gpu.bat` located in the "ComfyUI_windows_portable" folder to launch ComfyUI and access the GUI.
4. **Install comfyui_LLM_party**: Click the "Manager" button at the top right, navigate to `Custom Nodes manager`, then search for "party", and install the `comfyui_LLM_party` package.
5. **Import Custom Nodes**: Copy the `Supplementaries/comfyui_NoseNode` folder to `~\ComfyUI\custom_nodes`.
6. **Run ComfyUI Again**: Launch `run_nvidia_gpu.bat` again, and the ComfyUI GUI should now display.

### Running the Workflow
1. **Load Workflow**: Drag and drop the `Memoraid Update&Query Workflow.json` from the `Supplementaries/Workflows` folder into the ComfyUI GUI. (PS: Please Use your own API key.)
3. **Configure Database Directory**: Update the database directory paths as needed within the workflow. The personal profile file `Personal_info.json` and service information file `Service_info.json` can be found at `../Test_Data` and the corresponding path to those files should be adjsted based on your environment settings.
4. **Run Workflow**: Click "Queue Prompt" on the right side of the screen to execute the workflow.

### API Setup for Local Access
If you wish to run the workflow as an API on your local machine, follow these steps:

1. **Save API Format Workflow**: Ensure that the database directory is updated, as mentioned above.
2. **Enable Save as API Format**: Save your workflow in API format to generate a `.json` file.
3. **Add Workflow to API**: Place the `.json` file into `~\ComfyUI\custom_nodes\comfyui_LLM_party\workflow_api`.
4. **Launch FastAPI Server**: Run `setup_fastapi.bat` located in `~\ComfyUI\custom_nodes\comfyui_LLM_party`.
5. **Access API**: The workflow is now accessible in OpenAI API format. Use `http://127.0.0.1:8187/v1/chat/completions` as the URL, and set the model name to the name of your JSON file. The `API_KEY` can be ignored if not required.

### Example API Call
Here's an example for calling the workflow named `original_api.json`:
```python
import requests

url = "http://127.0.0.1:8187/v1/chat/completions"
headers = {"Content-Type": "application/json"}
payload = {
    "model": "original_api",
    "messages": [{"role": "user", "content": "How old am I again?"}]
}

response = requests.post(url, headers=headers, json=payload)
print(response.json())
```

## Notes
- The current setup leverages the visual workflow capabilities of ComfyUI for ease of use and transparency.
- Transitioning to a raw Python implementation is possible but requires additional effort and learning of the underlying structure.
- You can check the prompts for every agent in our workflow in the `Supplementaries/Prompts` folder.
