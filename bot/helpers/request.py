import requests
import json
from os import environ

from storage import redis


def use_headers(content_type="application/json", is_use_auth=False):
    headers = {"Content-type": content_type}

    if is_use_auth == True:
        headers.update({"Authorization": redis.get("access_token")})

    return headers


def create_post_request(path, data, is_use_auth=False):
    json_data = json.dumps(data)

    headers = use_headers(is_use_auth=is_use_auth)

    return requests.post(
        f"http://{environ.get('LOCAL_IP')}:8000/api/v1/{path}/",
        data=json_data,
        headers=headers,
    )


def create_get_request(path, params, is_use_auth=False):
    headers = use_headers(is_use_auth=is_use_auth)

    return requests.get(
        f"http://{environ.get('LOCAL_IP')}:8000/api/v1/{path}/",
        params=params,
        headers=headers,
    )
