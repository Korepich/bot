import requests
import json
from os import environ

from storage import redis


def create_post_request(path, data, is_use_auth = False):
    json_data = json.dumps(data)
    headers = {"Content-type": "application/json"}

    if is_use_auth == True:
        headers.update({"Authorization": redis.get("access_token")})

    return requests.post(
        f"http://{environ.get('LOCAL_IP')}:8000/api/v1/{path}/",
        data=json_data,
        headers=headers,
    )
