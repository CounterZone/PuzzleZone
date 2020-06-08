import json
from channels.generic.websocket import AsyncWebsocketConsumer

class PuzzleConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print(self.scope)
        await self.accept()
        

    def disconnect(self, close_code):
        print('disconnected.')
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        solution_code = text_data_json['solution']
        print(solution_code)
        for i in range(6):
            self.send(str(i))
