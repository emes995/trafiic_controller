from datetime import datetime
import json


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            encoded_object = {'_isoformat': obj.isoformat()}
        else:
            encoded_object = json.JSONEncoder.default(self, obj)
        return encoded_object


def customDecodeObjectHook(obj):
    _isoFormat = obj.get('_isoformat', None)
    if _isoFormat:
        return datetime.fromisoformat(_isoFormat)
    return obj
