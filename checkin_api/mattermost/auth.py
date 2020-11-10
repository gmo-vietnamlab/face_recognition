import requests
import json


def get_session_token():
    try:
        res = requests.post(url='https://chat.vietnamlab.vn/api/v4/users/login',
                            headers={
                            },
                            data=json.dumps({
                                'login_id': 'your_email',
                                'password': 'your_password'
                            }))
        print(res.headers, res.json())
        if res.status_code not in [200, 201]:
            print('http status code error', res.json(), res.status_code)
            return
    except Exception as e:
        print('Got exception when call api: ', e)
        return
    return res.headers['Token']


if __name__ == '__main__':
    get_session_token()
