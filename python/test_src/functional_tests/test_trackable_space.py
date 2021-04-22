import unittest

from controller.TrackableSpace import TrackableSpace
from controller.Controller import Controller
from controller.exceptions import MaxTrackableSpacePopulationException
from core.items.TrackableItem import TrackableItem
from core.location.ObjectLocation import ObjectLocation, Location


class TrackableSpaceTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._ctl = Controller()

    def test_controllableSpace(self):
        _cs = TrackableSpace(maxPopulation=10, name='Testing')
        for i in range(5):
            _longitude = Location(degree=40+i, minute=42, second=51, locationType=Location.LONGITUDE)
            _latitude = Location(degree=74+i, minute=0, second=21, locationType=Location.LATITUDE)
            _cs.addControllable(TrackableItem(objectLocation=ObjectLocation(latitude=_latitude,
                                                                            longitude=_longitude,
                                                                            height=0),
                                              controllable=True, name=f'name_{i}',
                                              parentController=self._ctl))

        self.assertEqual(len(_cs), 5)

    def test_controllable_exception(self):
        _cs = TrackableSpace(maxPopulation=10, name='Testing')
        try:
            for i in range(11):
                _longitude = Location(degree=40 + i, minute=42, second=51, locationType=Location.LONGITUDE)
                _latitude = Location(degree=74 + i, minute=0, second=21, locationType=Location.LATITUDE)
                _cs.addControllable(TrackableItem(objectLocation=ObjectLocation(latitude=_latitude,
                                                                                longitude=_longitude,
                                                                                height=0),
                                                  controllable=True, name=f'name_{i}',
                                                  parentController=self._ctl))
        except MaxTrackableSpacePopulationException as e:
            self.assertEqual(MaxTrackableSpacePopulationException, type(e))


if __name__ == '__main__':
    unittest.main()
