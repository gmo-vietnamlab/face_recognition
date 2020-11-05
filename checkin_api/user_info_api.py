import requests
from checkin_api.base_api import BaseAPI
from checkin_api.config import admin_user, admin_pass


class GetAllUserAPI(BaseAPI):
    def __init__(self):
        super().__init__()
        self.admin_token = self.get_token(user=admin_user, password=admin_pass)

    def call_api(self):
        """
        call checkin checkin_api
        :param username: ten nguoi nhan dang duoc
        :param checkin_time: thoi gian luc checkin
        :return: None
        """
        print(self.admin_token)
        try:
            res = requests.get(url=self.host + '/admin/get-all-user',
                                headers={
                                    'Authorization': f'Bearer {self.admin_token}',
                                    'Content-Type': 'application/json'
                                })
            if res.status_code != 200:
                print('http status code error', res.json(), res.status_code)

            return res.json()
        except Exception:
            print('got exception')
        # TODO: handle error by logging, or exception


# usage example
if __name__ == '__main__':
    # init instance (only one time)
    get_user_api = GetAllUserAPI()
    # call checkin_api checkin
    user_info = get_user_api.call_api()
    print(user_info)
