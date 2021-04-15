import unittest

from core.messages.ControllerMessage import ControllerMessage


class ControllerMessageTestCase(unittest.TestCase):

    def test_message(self):
        _pingMsg = ControllerMessage(messageType='PING', messagePayload={})
        self.assertEqual(_pingMsg.messageType, 'PING')

    def test_serialization(self):
        _originalMsg = ControllerMessage(messageType='ORIGINAL',
                                         messagePayload={'key': 'value'})
        _str = _originalMsg.toJson()
        _newMsg = ControllerMessage.fromJsonStr(_str)
        self.assertEqual(_newMsg.messageType, _originalMsg.messageType)
        self.assertDictEqual(_newMsg.messagePayload, _originalMsg.messagePayload)


if __name__ == '__main__':
    unittest.main()
