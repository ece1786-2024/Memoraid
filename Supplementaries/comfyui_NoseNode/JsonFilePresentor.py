import os
import json

class JsonFilePresentor:
    @classmethod
    def INPUT_TYPES(cls):
        return{
            "required": {
                "input_str": ("STRING",{}),
                "folder_path": ("STRING",{})
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("output",)
    FUNCTION = "present_json"
    CATEGORY = "CustomNodes/Test"

    def present_json(self, input_str, folder_path):
        debug_info = []
        try:
            input_data = json.loads(input_str)
            action = input_data["action"]
            file = input_data["file"]
            path = input_data["path"]
            new_value = input_data.get("new_value")
            
            # 添加调试信息
            debug_info.append(f"输入参数: action={action}, file={file}, path={path}, new_value={new_value}")
            
            result = f"""action is: {action}\nfile is: {file}\npath is: {path}\nnew_value is: {new_value}"""
            
            # 返回一个字典，符合 ComfyUI 的格式要求
            return {
                "ui": {"text": result},
                "result": (result,)
            }
        except json.JSONDecodeError as e:
            return {
                "ui": {"text": f"JSON解析错误：{str(e)}"},
                "result": (f"JSON解析错误：{str(e)}",)
            }
        except Exception as e:
            return {
                "ui": {"text": f"操作失败：{str(e)}"},
                "result": (f"操作失败：{str(e)}",)
            }