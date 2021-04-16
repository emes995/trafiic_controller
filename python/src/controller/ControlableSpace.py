import logging

from controller.exceptions import MaxControlableSpacePopulationException
from core.items.ControlableItem import ControlableItem


class ControlableSpace:

    def __init__(self, maxPopulation: int = -1):
        self._maxPopulation: int = maxPopulation
        self._population: dict = {}

    @property
    def maxPopulation(self):
        return self._maxPopulation

    def addControllable(self, controlableItem: ControlableItem, replace: bool=True):
        if not replace:
            if self._population.get(controlableItem.name, None):
                logging.warning(f'Element {controlableItem.name} already exists and will not be replaced')
                return

        if self._maxPopulation > -1:
            if len(self) >= self._maxPopulation:
                raise MaxControlableSpacePopulationException(f'Population already reached its limit {self._maxPopulation}')

        self._population[controlableItem.name] = controlableItem
        logging.debug(f'Adding {controlableItem.name} to space. Current length is {len(self)}')

    def removeControlableItem(self, name: str):
        assert isinstance(name, str), f'Expected str but got {type(name)}'
        try:
            _item = self._population.pop(name)
            logging.debug(f'Removing {name} to space. Current length is {len(self)}')
            return _item
        except KeyError as e:
            logging.error(f'Unable to find key {name}')

    def controlableItemExists(self, name: str):
        return self._population.get(name, False)

    def __len__(self):
        return len(self._population)

    def __repr__(self):
        return f'{type(self)}'

