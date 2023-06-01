from redis import Redis
from os import environ

redis = Redis(host=environ.get('LOCAL_IP'), port=6379, decode_responses=True)
