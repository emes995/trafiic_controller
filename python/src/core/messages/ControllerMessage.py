import datetime
import uuid
import json

from utils.OrderedIdGenerator import OrderedIdGenerator
from utils.jsonutils import customDecodeObjectHook, CustomEncoder


class ControllerMessage:

    def __init__(self, messageType: str,
                 messagePayload: dict):
        self._id = OrderedIdGenerator.generate_ordered_id(f'{uuid.uuid4()}')
        self._timestamp = datetime.datetime.now()
        self._msgType = messageType
        self._msgPayload = messagePayload

    @property
    def messageType(self):
        return self._msgType

    @property
    def messagePayload(self):
        return self._msgPayload

    @staticmethod
    def fromJsonStr(jsonStr: str):
        _msgDict = json.loads(jsonStr, object_hook=customDecodeObjectHook)
        _rootMsg = _msgDict.get('message')
        _msg = ControllerMessage(messageType=_rootMsg.get('type'),
                                 messagePayload=_rootMsg.get('payload'))
        return _msg

    def isException(self):
        return self.messageType == 'EXCEPTION'

    def toJson(self):
        return json.dumps({
            'message': {
                'id': self._id,
                'type': self._msgType,
                'timestamp': self._timestamp,
                'payload': self._msgPayload
            }
        }, cls=CustomEncoder)
