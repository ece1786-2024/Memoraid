from .JsonFileQuerier import JsonFileQuerier
from .JsonFilePresentor import JsonFilePresentor
from .OutputJudge import VoteBasedRouter
from .JsonFileUpdator import JsonFileUpdator

NODE_CLASS_MAPPINGS = {
    "JsonFileQuerier": JsonFileQuerier,
    "JsonFilePresentor": JsonFilePresentor,
    "VoteBasedRouter": VoteBasedRouter,
    "JsonFileUpdator": JsonFileUpdator
}

NODE_DISPLAY_NAMES_MAPPINGS = {
    "JsonFileQuerier": "Data - JSON File Querier",
    "JsonFilePresentor": "Test - JSON File Presentor",
    "VoteBasedRouter": "Decision - Vote Based Router",
    "JsonFileUpdator": "Data - JSON File Updator"
}
