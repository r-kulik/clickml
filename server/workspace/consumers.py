from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json


class ExploitLoadingConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.task_id = -2

    def connect(self):
        self.accept()
        async_to_sync(self.channel_layer.group_add)("waiting_results", self.channel_name)

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)("waiting_results", self.channel_name)

    def receive(self, text_data=None, bytes_data=None):
        print('I received a nice message!')
        json_data = json.loads(text_data)
        self.task_id = int(json_data.get('task_id'))

    def results_get(self, event: dict) -> None:
        if event.get('type', 'undefined') == 'results.get':
            data = json.loads(event.get('text', '{}'))
            task_id = data.get('task_id', 0)
            print(f"from consumer: finished task_id is {data.get('task_id', 0)}")
            if data.get('task_id', 0) == self.task_id:
                self.send(text_data=json.dumps(
                    {
                        'finish': 1,
                        "task_id": self.task_id
                    }
                ))


class LearningLoadingConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.learning_task_id_list = []

    def connect(self):
        self.accept()
        async_to_sync(self.channel_layer.group_add)("waiting_learning_task_info",
                                                    self.channel_name)

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)("waiting_learning_task_info",
                                                        self.channel_name)

    def receive(self, text_data=None, bytes_data=None):
        json_data = json.loads(text_data)
        # print(f"JSON DATA GET LEARNING_TASK = {json_data.get}
        print(json_data)
        self.learning_task_id_list = json_data.get('learning_task_id_list')
        print(self.learning_task_id_list)
        print(type(self.learning_task_id_list))
        print(f"CONSUMER GOT LEARNING_TASKID_LIST = {self.learning_task_id_list}")

    def info_get(self, event: dict) -> None:

        if event.get('type', 'undefined') == "info.get":
            data = json.loads(event.get('text', '{}'))
            learning_task_id = data.get('learning_task_id', -1)
            if int(learning_task_id) in self.learning_task_id_list:
                print("WANNA SEND A MESSAGE")
                self.send(
                    text_data=event.get('text', '{}')
                )

    def complete(self, event:dict) -> None:
        if event.get('type', 'undefined') == "complete":
            data = json.loads(event.get("text", "{}"))
            learning_task_id = data.get('learning_task_id', -1)
            ml_model_id = data.get('ml_model_id', -1)
            if int(learning_task_id) in self.learning_task_id_list:
                json_data = {
                    "learning_task_id": learning_task_id,
                    "complete": 1,
                    "ml_model_id": ml_model_id
                }
                self.send(
                    text_data=json.dumps(json_data)
                )