from uuid import uuid4
from utils.OrderedIdGenerator import OrderedIdGenerator


class ControllableItem:

    def __init__(self, controllable: bool, name: str, parentController):
        self._isControllable: bool = controllable
        self._id = OrderedIdGenerator.generate_ordered_id(f'{uuid4()}')
        self._name = name
        self._parentController = parentController

    @property
    def name(self):
        return self._name

    @property
    def isControllable(self):
        return self._isControllable

    def acquireControl(self, newController):
        self._parentController.releaes()
        self._parentController = newController

    def releaseControl(self):
        self._parentController.releaseControl()
