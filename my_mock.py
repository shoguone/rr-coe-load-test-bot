import json

class MyMock:
    def __init__(self):
        init_response_f = open('init-response.json', 'r')
        init_response_str = init_response_f.read()
        self.init_response = json.loads(init_response_str)

    def get_init_response(self):
        return self.init_response