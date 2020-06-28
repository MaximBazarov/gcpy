import json


def binary_decode(body):
    return json.loads(body.decode("UTF-8"))


def str_to_dict(data):
    return json.loads(data)


def binary_encode(payload: dict):
    return json.dumps(payload).encode()
