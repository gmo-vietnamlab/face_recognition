import requests
from abc import abstractmethod
import json


class BaseAPI:
    host = 'http://150.95.173.159:8585/api'

    def __init__(self):
        pass

    @abstractmethod
    def call_api(self, args):
        pass

    def get_token(self, user, password):
        try:
            res = requests.post(url=self.host + '/users/login',
                                data=json.dumps({
                                    "user": {
                                        "email": user,
                                        "password": password
                                    }
                                }),
                                headers={'Content-Type': 'application/json'})
            if res.status_code != 200:
                print('http status code error', res.json(), res.status_code)
            return res.json()['user']['token']
        except Exception:
            print('got exception base api')
