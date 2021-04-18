import asyncio
import logging

from controller.ControllableSpace import ControllableSpace
from core.items.ControllableItem import ControllableItem
from utils.OrderedIdGenerator import OrderedIdGenerator
from uuid import uuid4
from core.messages.ControllerMessage import ControllerMessage


class Controller:

    def __init__(self):
        self._id = OrderedIdGenerator.generate_ordered_id(f'{uuid4()}')
        self._started = False
        self._stopped = False
        self._controllableSpaces: dict = {}

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

    def addControllableSpace(self, ctlSpace: ControllableSpace):
        self._controllableSpaces[ctlSpace.name] = ctlSpace

    async def ping(self) -> ControllerMessage:
        if self._stopped:
            return ControllerMessage(messageType='EXCEPTION',
                                     messagePayload={'message': 'Controller has already been stopped'})
        return ControllerMessage(messageType='PONG', messagePayload={})

    def addControllableItem(self, controllableItem: ControllableItem, ctlSpace: str):
        _ctlSpace = self._controllableSpaces.get(ctlSpace)
        _ctlSpace.addControllable(controllableItem=controllableItem)

    def removeControllableItem(self, name: str, ctlSpace: str):
        _ctlSpace = self._controllableSpaces.get(ctlSpace)
        _ctlSpace.removeControllableItem(name)

    def getControllablePopulation(self, ctlSpace: str):
        _ctlSpace = self._controllableSpaces.get(ctlSpace)
        return len(_ctlSpace)

    async def start(self):
        logging.info(f'Starting controller {self._id}')
        self.controllerStarted = True
        while not self.controllerStop:
            for _k, _v in self._controllableSpaces.items():
                _cs: ControllableSpace = _v
                logging.debug(f'ControllableSpace {_k} has {len(_cs)}')
            await asyncio.sleep(0.1)

        logging.info('Controller has stopped')

    async def stop(self):
        logging.info(f'Stopping controller {self._id}')
        self.controllerStop = True

    def __str__(self):
        return f'{type(self)}'
