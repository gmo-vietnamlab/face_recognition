import requests
import json
import os
from checkin_api.mattermost.auth import get_session_token
from checkin_api.config import mattermost_token


def post_message_to_channel(message):
    token = mattermost_token
    res = requests.post(url='https://chat.vietnamlab.vn/api/v4/posts',
                        headers={
                            'Authorization': f'Bearer {token}',
                            'Content-Type': 'application/json',
                        },
                        data=json.dumps({
                            "channel_id": "n3oyx6upyi86jjcixc65hdbkqc",
                            "message": message,
                            "file_ids": [
                            ],
                            "props": {}
                        }))
    print(res.status_code, res.json())


if __name__ == '__main__':
    post_message_to_channel()
