import logging

from controller.exceptions import MaxControllableSpacePopulationException
from core.items.ControllableItem import ControllableItem


class ControllableSpace:

    def __init__(self, maxPopulation: int = -1):
        self._maxPopulation: int = maxPopulation
        self._population: dict = {}

    @property
    def maxPopulation(self):
        return self._maxPopulation

    def addControllable(self, controllableItem: ControllableItem, replace: bool = True):
        if not replace:
            if self._population.get(controllableItem.name, None):
                logging.warning(f'Element {controllableItem.name} already exists and will not be replaced')
                return

        if self._maxPopulation > -1:
            if len(self) >= self._maxPopulation:
                raise MaxControllableSpacePopulationException(f'Population already reached its limit'
                                                              f' {self._maxPopulation}')

        self._population[controllableItem.name] = controllableItem
        logging.debug(f'Adding {controllableItem.name} to space. Current length is {len(self)}')

    def removeControllableItem(self, name: str):
        assert isinstance(name, str), f'Expected str but got {type(name)}'
        try:
            _item = self._population.pop(name)
            logging.debug(f'Removing {name} to space. Current length is {len(self)}')
            return _item
        except KeyError:
            logging.error(f'Unable to find key {name}')

    def controllableItemExists(self, name: str):
        return self._population.get(name, False)

    def __len__(self):
        return len(self._population)

    def __repr__(self):
        return f'{type(self)}'
