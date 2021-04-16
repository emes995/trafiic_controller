import unittest

from controller.ControllableSpace import ControllableSpace
from controller.Controller import Controller
from controller.exceptions import MaxControllableSpacePopulationException
from core.items.ControllableItem import ControllableItem
from core.location.ObjectLocation import ObjectLocation, Location


class ControllableSpaceTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._ctl = Controller()

    def test_controllableSpace(self):
        _cs = ControllableSpace(maxPopulation=10)
        for i in range(5):
            _longitude = Location(degree=40+i, minute=42, second=51, locationType=Location.LONGITUDE)
            _latitude = Location(degree=74+i, minute=0, second=21, locationType=Location.LATITUDE)
            _cs.addControllable(ControllableItem(objectLocation=ObjectLocation(latitude=_latitude,
                                                                               longitude=_longitude,
                                                                               height=0),
                                                 controllable=True, name=f'name_{i}',
                                                 parentController=self._ctl))

        self.assertEqual(len(_cs), 5)

    def test_controllable_exception(self):
        _cs = ControllableSpace(maxPopulation=10)
        try:
            for i in range(11):
                _longitude = Location(degree=40 + i, minute=42, second=51, locationType=Location.LONGITUDE)
                _latitude = Location(degree=74 + i, minute=0, second=21, locationType=Location.LATITUDE)
                _cs.addControllable(ControllableItem(objectLocation=ObjectLocation(latitude=_latitude,
                                                                                   longitude=_longitude,
                                                                                   height=0),
                                                     controllable=True, name=f'name_{i}',
                                                     parentController=self._ctl))
        except MaxControllableSpacePopulationException as e:
            self.assertEqual(MaxControllableSpacePopulationException, type(e))


if __name__ == '__main__':
    unittest.main()
