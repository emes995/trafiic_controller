import asyncio
import logging
import aiounittest

from controller.Controller import Controller, ControllerWatcher
from controller.exceptions import ControllerStoppedException
from python.test_src.CustomTestCase import CustomTestCase
from core.messages.ControllerMessage import ControllerMessage


class ControllerTestCase(CustomTestCase):

    @staticmethod
    async def stop_controller(controller: Controller):
        await asyncio.sleep(10)
        logging.info('Starting to stop controller')
        await controller.stop()

    @staticmethod
    async def ping_controller(controller: Controller):
        while True:
            await asyncio.sleep(1.0)
            _ping: ControllerMessage = await controller.ping()
            if _ping.isException():
                raise ControllerStoppedException(_ping.messagePayload.get('message'))
            logging.info(f'{_ping.messageType}')

    @staticmethod
    async def test_controller():
        _ctl = Controller()
        _ctlTask = asyncio.ensure_future(_ctl.start())
        _stopCtlTask = asyncio.ensure_future(ControllerTestCase.stop_controller(controller=_ctl))
        _pingTask = asyncio.ensure_future(ControllerTestCase.ping_controller(controller=_ctl))
        _watchCtl = asyncio.ensure_future(ControllerWatcher(sleepInterval=0.3, controller=_ctl).start())

        await _ctlTask
        await _stopCtlTask
        try:
            await _pingTask
            await _watchCtl
        except Exception as e:
            logging.exception(e)
        logging.info('Test completed')


if __name__ == '__main__':
    aiounittest.main()
