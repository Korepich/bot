import math
from dateutil import parser

from storage import redis
from helpers import create_get_request


def read_history():
    current_page = redis.get("history_pages_current")

    if current_page == None:
        redis.set("history_pages_current", 1)

    current_page = 1

    response = create_get_request("action/list", {"page": current_page}).json()

    page_quantity = math.ceil(response["count"] / 5)

    redis.set("history_pages_quantity", page_quantity)

    history = ""

    for item in response["results"]:
        action = "открыть" if item["is_open"] == True else "закрыть"
        date = parser.parse(item["created"])

        history += f"Действие: {action}\nВремя {date.day}.{date.month}.{date.year} {date.hour}:{date.minute}\n\n"
    
    return history
