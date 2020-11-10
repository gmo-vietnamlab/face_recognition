import requests
import json
from checkin_api.mattermost.auth import get_session_token


def create_bot():
    session_token = get_session_token()
    res = requests.post(url='https://chat.vietnamlab.vn/api/v4/bots',
                        headers={
                            'Authorization': f'Bearer {session_token}',
                            'Content-Type': 'application/json',
                        },
                        data=json.dumps({
                            "username": "CheckinBot",
                            "display_name": "CheckinBot",
                            "description": "Bot to used for checkin"
                        }))
    print(res.status_code, res.json(), res.headers)


create_bot()
