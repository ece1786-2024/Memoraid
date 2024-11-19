import os
import json

# The input_str is like follow structures:
"""
{
       "action": "update",
       "file": "Service_info",
       "path": "facility[name='Recreation Room'].location",
       "new_value": "Third Floor, North Wing"
}
"""
#该节点将返回一个字符串，表示查询结果。
class JsonFileQuerier:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_str": ("STRING", {}),
                "folder_path": ("STRING", {}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("output",)
    FUNCTION = "manipulate_json"
    CATEGORY = "CustomNodes/Data"

    def _parse_path(self, data, path_str):
        """解析JSON路径并返回对应的值
        Args:
            data: JSON数据
            path_str: 路径字符串 (例如: "facility[name='Recreation Room'].location")
        Returns:
            找到的值
        """
        parts = path_str.split('.')
        current = data
        debug_info = []  # 用于收集路径解析的调试信息
        
        for part in parts:
            debug_info.append(f"当前部分: {part}, 当前数据: {current}")
            if '[' in part and ']' in part:
                array_name = part.split('[')[0]
                condition = part[part.index('[')+1:part.index(']')]
                key, value = condition.split('=')
                value = value.strip("'\"")
                
                if isinstance(current.get(array_name), list):
                    for item in current[array_name]:
                        if item.get(key) == value:
                            current = item
                            break
                    else:
                        raise ValueError(f"找不到匹配的项: {condition}")
                else:
                    raise ValueError(f"{array_name} 不是一个列表")
            else:
                if part in current:
                    current = current[part]
                else:
                    raise ValueError(f"路径部分 '{part}' 不存在")
        
        debug_info.append(f"最终结果: {current}")
        print("\n".join(debug_info))  # 打印调试信息
        return current

    def manipulate_json(self, input_str, folder_path):
        debug_info = []  # 用于收集调试信息
        try:
            # Step 1: Parse the input string
            input_data = json.loads(input_str)
            action = input_data["action"]
            file = input_data["file"]
            path = input_data["path"]
            debug_info.append(f"输入参数: action={action}, file={file}, path={path}")

            # Step 2: Construct the full file path
            file_path = os.path.join(folder_path, f"{file}.json")
            debug_info.append(f"文件路径: {file_path}")
            
            if not os.path.exists(file_path):
                error_message = f"错误：文件不存在 - {file_path}"
                return {"ui": {"text": error_message}, "result": (error_message,)}

            # Step 3: Load the JSON file
            with open(file_path, "r", encoding='utf-8') as f:
                data = json.load(f)
                debug_info.append(f"成功读取文件，数据结构: {list(data.keys())}")  # 只显示顶层键

            # Step 4: Perform action (query/update)
            if action == "query":
                try:
                    result = self._parse_path(data, path)
                    debug_info.append(f"查询结果原始数据: {result}")
                    
                    # 格式化返回结果
                    if result is None:
                        final_result = "未找到匹配数据"
                    elif isinstance(result, (dict, list)):
                        final_result = json.dumps(result, ensure_ascii=False, indent=2)
                    else:
                        final_result = str(result)
                    
                    # 组合调试信息和结果
                    output_text = "\n".join([
                        "=== 调试信息 ===",
                        *debug_info,
                        "\n=== 查询结果 ===",
                        final_result
                    ])
                    return {"ui": {"text": output_text}, "result": (final_result,)}
                except Exception as e:
                    error_message = f"查询出错: {str(e)}"
                    return {"ui": {"text": error_message}, "result": (error_message,)}
            else:
                # 返回空值
                return {"ui": {"text": "操作类型不是查询，返回空值"}, "result": ("",)}

        except json.JSONDecodeError as e:
            error_message = f"JSON解析错误：{str(e)}"
            return {"ui": {"text": error_message}, "result": (error_message,)}
        except Exception as e:
            error_message = f"操作失败：{str(e)}"
            return {"ui": {"text": error_message}, "result": (error_message,)}
    
    