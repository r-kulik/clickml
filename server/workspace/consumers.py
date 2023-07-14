from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class ExploitLoadingConsumer(WebsocketConsumer):

    def connect(self):
        self.accept()
        async_to_sync(self.channel_layer.group_add)("waiting_results", self.channel_name)

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)("waiting_results", self.channel_name)

    def receive(self, text_data=None, bytes_data=None):
        print('I received a nice message!')
        print(text_data)

    def results_get(self, event) -> None:
        print("I GOT THE BROADCAST MESSAGE SUUKA")
        print(event)
