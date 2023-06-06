from helpers.request import create_post_request
import json
from os import environ
import threading
from datetime import timedelta

from helpers import base64_decode
from storage import redis


def refresh_token():
    threading.Timer(int(environ.get("ACCESS_TTL")) * 60, refresh_token).start()

    response = create_post_request(
        "token/refresh", {"refresh": redis.get("refresh_token")}
    )

    redis.set(
        "access_token",
        environ.get("JWT_SECRET_WORD") + " " + response.json()["access"],
    )


def authentication(data):
    response = create_post_request(
        "token", {"username": data["login"], "password": data["password"]}
    )

    if response.status_code == 200:
        base64_token = response.json()["access"].split(".")
        user_id = json.loads(base64_decode(base64_token[1]))["user_id"]

        redis.set("user_id", user_id)
        redis.set("refresh_token", response.json()["refresh"])
        redis.set(
            "access_token",
            environ.get("JWT_SECRET_WORD") + " " + response.json()["access"],
        )

        refresh_token()

        return True

    return False
