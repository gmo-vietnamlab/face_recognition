import requests
import json
from checkin_api.base_api import BaseAPI
from checkin_api.config import admin_user, admin_pass


class CheckinAPI(BaseAPI):
    def __init__(self):
        super().__init__()
        self.admin_token = self.get_token(user=admin_user, password=admin_pass)

    def call_api(self, username, checkin_time='2020-05-16T15:24:01+07:00'):
        """
        call checkin checkin_api
        :param username: ten nguoi nhan dang duoc
        :param checkin_time: thoi gian luc checkin
        :return: None
        """
        print(username, checkin_time)
        try:
            res = requests.post(url=self.host + '/admin/checkin-by-username',
                                headers={
                                    'Authorization': f'Bearer {self.admin_token}',
                                    'Content-Type': 'application/json'
                                },
                                data=json.dumps({
                                    "username": username,
                                    "check_in_time": checkin_time
                                }))
            if res.status_code not in [200, 201]:
                print('http status code error', res.json(), res.status_code)
        except Exception:
            print('got exception check in api')
        # TODO: handle error by logging, or exception


# usage example
if __name__ == '__main__':
    # init instance (only one time)
    checkin_api = CheckinAPI()
    # call checkin_api checkin
    checkin_api.call_api('jack')
