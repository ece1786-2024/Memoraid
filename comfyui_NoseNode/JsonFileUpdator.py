import os
import json

class JsonFileUpdator:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_str": ("STRING", {}),
                "folder_path": ("STRING", {}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("updated_content",)
    FUNCTION = "update_json_file"
    CATEGORY = "CustomNodes/Data"

    def update_json_file(self, input_str, folder_path):
        # Check if input_str or folder_path is None
        if input_str == "" or folder_path == "":
            return ""
        try:
            # Step 1: Parse the input string
            input_data = json.loads(input_str)
            file_name = input_data["file"]
            path = input_data["path"]
            new_content = input_data["new_content"]

            # Step 2: Construct the full file path
            file_path = os.path.join(folder_path, f"{file_name}.json")

            if not os.path.exists(file_path):
                error_message = f"错误：文件不存在 - {file_path}"
                return {"ui": {"text": error_message}, "result": (error_message,)}

            # Step 3: Load the JSON file
            with open(file_path, "r", encoding='utf-8') as f:
                data = json.load(f)

            # Step 4: Update the specified path with new content
            if path in data:
                data[path] = new_content
            else:
                error_message = f"路径 '{path}' 不存在于文件中"
                return {"ui": {"text": error_message}, "result": (error_message,)}

            # Step 5: Save the updated JSON back to the file
            with open(file_path, "w", encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            # Step 6: Return the updated content
            updated_content = json.dumps(data[path], ensure_ascii=False, indent=2)
            return {"ui": {"text": "更新成功"}, "result": (updated_content,)}

        except json.JSONDecodeError as e:
            error_message = f"JSON解析错误：{str(e)}"
            return {"ui": {"text": error_message}, "result": (error_message,)}
        except Exception as e:
            error_message = f"操作失败：{str(e)}"
            return {"ui": {"text": error_message}, "result": (error_message,)}
