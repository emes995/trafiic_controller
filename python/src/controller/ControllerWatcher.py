import asyncio
import logging

from controller.exceptions import ControllerStoppedException


class ControllerWatcher:

    def __init__(self, sleepInterval: float = 0.01, controller=None):
        self._controller = controller
        self._sleepInterval = sleepInterval
        self._stopped = False

    async def start(self):
        while not self._stopped:
            await asyncio.sleep(self._sleepInterval)
            if self._controller.controllerStarted:
                logging.info(f'Sending PING to {self._controller}')
                _pingMsg = await self._controller.ping()
                if _pingMsg.isException():
                    raise ControllerStoppedException(_pingMsg.messagePayload.get('message'))
                logging.info(f'{_pingMsg.messageType}')

        logging.info('Stopping ControllerWatcher')

    async def stop(self):
        self._stopped = True
