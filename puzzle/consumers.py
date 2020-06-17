import json
from channels.generic.websocket import AsyncWebsocketConsumer

class PuzzleConsumer(AsyncWebsocketConsumer):
    '''
    deal with the websocket created by the user.
    the solution code is sent through the websocket. the server would send messages about the test.
    the 'submission' command also send through the socket. the server would accept the submission only when the test is passed.
    '''
    async def connect(self):
        print(self.scope)
        self.accept()
    async def disconnect(self, close_code):
        print('disconnected.')
        pass
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        solution_code = text_data_json['solution']
        print(solution_code)
        for i in range(6):
            self.send(str(i))
