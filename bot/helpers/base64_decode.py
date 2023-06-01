import base64

def base64_decode(str):
    str = bytes(str, 'utf-8')
    return base64.b64decode(str + b'=' * (-len(str) % 4))
