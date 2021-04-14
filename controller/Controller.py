from controller import PriorityControl
import logging


class Controller:

    def __init__(self, loop=None):
        self._loop = loop
        self._priorityController = dict()

    def addController(self, priorityController:  PriorityControl):
        self._priorityController[priorityController.priority] = priorityController

    def removeController(self, priority):
        priorityController: PriorityControl = self._priorityController.get(priority, None)
        if not priority:
            logging.info(f'Controller with priorirty {priority} not found')
        return priorityController

    def __len__(self):
        return len(self._priorityController)

    def __repr__(self):
        return f'{type(self)}'

    def start(self):
        pass

    def stop(self):
        pass

    def pause(self):
        pass
