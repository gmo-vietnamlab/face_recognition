import requests
from abc import abstractmethod
import json
import os
from checkin_api.config import api_host


class BaseAPI:
    host = api_host

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
