import asyncio
import logging

from utils.OrderedIdGenerator import OrderedIdGenerator
from uuid import uuid4
from core.messages.ControllerMessage import ControllerMessage


class ControllerWatcher:

    def __init__(self, sleepInterval: float = 0.01, controller=None):
        self._controller = controller
        self._sleepInterval = sleepInterval
        self._stopped = False

    async def start(self):
        while not self._stopped:
            await asyncio.sleep(self._sleepInterval)
            if self._controller.controllerStarted:
                _pingMsg = ControllerMessage.fromJsonStr(self._controller.ping())

        logging.info('Stopping ControllerWatcher')

    async def stop(self):
        self._stopped = True


class Controller:

    class ControllerArtifact:
        def __init__(self, sleepInterval: float = 0.75, controller=None):
            self._stopped = False
            self._sleepInterval = sleepInterval
            self._controller = controller

        async def start(self):
            logging.info('Starting Controller')
            while not self._stopped:
                logging.info('Monitor still watching')
                await asyncio.sleep(self._sleepInterval)

            logging.info('Controller Artifact has stopped')

        async def stop(self):
            logging.info('Stopping Controller Artifact')
            self._stopped = True

    def __init__(self):
        self._id = OrderedIdGenerator.generate_ordered_id(f'{uuid4()}')
        self._started = False
        self._stopped = False
        self._controllerArtifactFuture = None

    @property
    def controllerStarted(self) -> bool:
        return self._started

    @property
    def controllerStop(self):
        return self._stopped

    @controllerStop.setter
    def controllerStop(self, value: bool):
        self._stopped = value

    async def ping(self) -> ControllerMessage:
        if self._stopped:
            return ControllerMessage(messageType='EXCEPTION',
                                     messagePayload={'message': 'Controller has already been stopped'})
        return ControllerMessage(messageType='PONG', messagePayload={})

    async def start(self):
        logging.info(f'Starting controller {self._id}')
        _ctlWatcher = Controller.ControllerArtifact(controller=self)
        self._controllerArtifactFuture = asyncio.ensure_future(_ctlWatcher.start())
        self._controllerArtifactFuture.add_done_callback(self.stop)
        while not self.controllerStop:
            logging.info('Controller going....')
            await asyncio.sleep(0.5)

        await _ctlWatcher.stop()
        logging.info('Controller has stopped')

    async def stop(self):
        logging.info(f'Stopping controller {self._id}')
        self.controllerStop = True
