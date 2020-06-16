import json
from channels.generic.websocket import WebsocketConsumer
from .docker_test import atest
class PuzzleConsumer(WebsocketConsumer):
    def connect(self):
        print(self.scope)
        self.accept()


    def disconnect(self, close_code):
        print('disconnected.')
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        solution_code = text_data_json['solution']

        for i in range(2):
            a=atest()
            print(type(a))
            self.send(str(a))
        self.close()
