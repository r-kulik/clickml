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
        # print("I GOT THE BROADCAST MESSAGE SUUKA")
        if event.get('type', 'undefined') == 'results.get':
            data = json.loads(event.get('text', '{}'))
            task_id = data.get('task_id', 0)
            print(f"from consumer: finished task_id is {data.get('task_id', 0)}")
            if data.get('task_id', -1) == self.task_id:
                self.send(text_data=json.dumps(
                    {
                        'finish': 1,
                        "task_id": self.task_id
                    }
                ))