import json

class VoteBasedRouter:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "user_input": ("STRING", {}),
                "voted_reply": ("STRING", {}),
                "json_input_1": ("STRING", {}),
                "json_input_2": ("STRING", {}),
                "json_input_3": ("STRING", {}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("vote>=2", "vote<2")
    FUNCTION = "route_based_on_votes"
    CATEGORY = "CustomNodes/Decision"

    def route_based_on_votes(self, user_input, voted_reply, json_input_1, json_input_2, json_input_3):
        try:
            # Parse the JSON inputs
            data_1 = json.loads(json_input_1)
            data_2 = json.loads(json_input_2)
            data_3 = json.loads(json_input_3)

            # Calculate the total votes
            total_votes = data_1.get("vote", 0) + data_2.get("vote", 0) + data_3.get("vote", 0)

            # Determine the output based on the total votes
            if total_votes >= 2:
                return {
                    "ui": {"text": "Vote total is >= 2"},
                    "result": (voted_reply, "")#表示投票通过，可采用该reply，输出到第一个端口
                }
            else:
                return {
                    "ui": {"text": "Vote total is < 2"},
                    "result": ("", user_input)#表示投票不通过，需要将用户的原始问题传回开头重新跑流程 ,输出到第二个端口
                }

        except json.JSONDecodeError as e:
            error_message = f"JSON解析错误：{str(e)}"
            return {
                "ui": {"text": error_message},
                "result": (error_message, error_message)
            }
        except Exception as e:
            error_message = f"操作失败：{str(e)}"
            return {
                "ui": {"text": error_message},
                "result": (error_message, error_message)
            }
