import datetime
import json
import unittest
from utils.jsonutils import CustomEncoder, customDecodeObjectHook


class MyTestCase(unittest.TestCase):
    def test_json_date_encode(self):
        _obj = {'date': datetime.datetime.now(),
                'test': 'testing'
                }
        _strEnc = json.dumps(_obj, cls=CustomEncoder)
        _objDec = json.loads(_strEnc, object_hook=customDecodeObjectHook)
        self.assertEqual(_obj, _objDec)

    def test_json_date_decode(self):
        _jsonStr = '{"date": {"_isoformat": "2021-04-14T22:23:19.158611"}, "test": "testing"}'
        _obj = {'date': datetime.datetime(2021, 4, 14, 22, 23, 19, 158611),
                'test': 'testing'
                }
        _objDec = json.loads(_jsonStr, object_hook=customDecodeObjectHook)
        self.assertEqual(_obj, _objDec)

if __name__ == '__main__':
    unittest.main()
