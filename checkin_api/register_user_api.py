import requests
import json
from checkin_api.base_api import BaseAPI
from checkin_api.config import admin_user, admin_pass


class RegisterUserAPI(BaseAPI):
    def __init__(self):
        super().__init__()
        self.admin_token = self.get_token(user=admin_user, password=admin_pass)

    def call_api(self, username, email, password):
        """
        call checkin checkin_api
        :param username: ten nguoi nhan dang duoc
        :param checkin_time: thoi gian luc checkin
        :return: None
        """
        print(self.admin_token)
        try:
            res = requests.post(url=self.host + '/users/signup',
                                headers={
                                    'Authorization': f'Bearer {self.admin_token}',
                                    'Content-Type': 'application/json'
                                },
                                data=json.dumps({
                                    "user": {
                                        "username": username,
                                        "email": email,
                                        "password": password
                                    }
                                }))
            if res.status_code not in [200, 201]:
                print('http status code error', res.json(), res.status_code)

        except Exception:
            print('got exception')
        # TODO: handle error by logging, or exception


# usage example
if __name__ == '__main__':
    # init instance (only one time)
    register_user_api = RegisterUserAPI()
    # call checkin_api checkin
    register_user_api.call_api('NguyenBaDuy', 'duynb@vietnamlab.vn', '123@abc')
    register_user_api.call_api('NguyenTuanAnh', 'anhnt92@vietnamlab.vn', '123@abc')
    register_user_api.call_api('NguyenVanThai', 'thainv@vietnamlab.vn', '123@abc')
    register_user_api.call_api('PhamHieuTrung', 'trungph@vietnamlab.vn', '123@abc')
    register_user_api.call_api('PhamVanDong', 'dongpv@vietnamlab.vn', '123@abc')
    register_user_api.call_api('TranCaoQuy', 'quytc@vietnamlab.vn', '123@abc')
    register_user_api.call_api('TranThanhTung', 'tungtt1@runsystem.net', '123@abc')
    register_user_api.call_api('TranTrungThanh', 'thanhtt@vietnamlab.vn', '123@abc')
    register_user_api.call_api('VuHongVan', 'vanvh@vietnamlab.vn', '123@abc')
    register_user_api.call_api('VuNgocHoan', 'hoanvn@vietnamlab.vn', '123@abc')


