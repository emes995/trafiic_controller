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
    _isoformat = obj.get('_isoformat', None)
    if _isoformat:
        return datetime.fromisoformat(_isoformat)
    return obj


#if __name__ == '__main__':
    #d = { 'now': datetime(2000, 1, 1) }
    #d = { 'now': datetime(2000, 1, 1, tzinfo=timezone(timedelta(hours=-8))) }
    #s = json.dumps(d, default=default)
    #print(s)
    #print(d == json.loads(s, object_hook=object_hook))
