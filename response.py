from enum import Enum

from flask import jsonify


class ResponseCode(Enum):
    SUCCESS = 200
    BAD_REQUEST = 400
    INTERNAL_SERVER_ERROR = 500


class Response:
    def __init__(self, data=None, code=ResponseCode.SUCCESS, msg="ok"):
        self.data = data
        self.code = code.value
        self.msg = f'[{code.name}] {msg}'

    def json(self):
        return jsonify({
            'code': self.code,
            'messages': self.msg,
            'data': self.data
        })
