import asyncio
import logging

from controller.ControllableSpace import ControllableSpace
from controller.exceptions import ControllerStoppedException
from core.items.ControllableItem import ControllableItem
from utils.OrderedIdGenerator import OrderedIdGenerator
from uuid import uuid4
from core.messages.ControllerMessage import ControllerMessage


class ControllerWatcher:

    def __init__(self, sleepInterval: float = 0.01, controller=None):
        self._controller = controller
        self._sleepInterval = sleepInterval
        self._stopped = False
        self._controllableSpace = ControllableSpace(maxPopulation=10)

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


class Controller:

    def __init__(self):
        self._id = OrderedIdGenerator.generate_ordered_id(f'{uuid4()}')
        self._started = False
        self._stopped = False
        self._controllableSpace = ControllableSpace(maxPopulation=50)

    @property
    def controllerStarted(self) -> bool:
        return self._started

    @controllerStarted.setter
    def controllerStarted(self, value: bool):
        self._started = value

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

    def addControllableItem(self, controlableItem: ControllableItem):
        self._controllableSpace.addControllable(controllableItem=controlableItem)

    def removeControllableItem(self, name: str):
        self._controllableSpace.removeControllableItem(name)

    def getControllablePopulation(self):
        return len(self._controllableSpace)

    async def start(self):
        logging.info(f'Starting controller {self._id}')
        self.controllerStarted = True
        while not self.controllerStop:
            logging.debug('Controller going....')
            await asyncio.sleep(0.5)

        logging.info('Controller has stopped')

    async def stop(self):
        logging.info(f'Stopping controller {self._id}')
        self.controllerStop = True

    def __str__(self):
        return f'{type(self)}'
