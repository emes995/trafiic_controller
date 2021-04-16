import unittest

from controller.ControllableSpace import ControllableSpace
from controller.Controller import Controller
from controller.exceptions import MaxControllableSpacePopulationException
from core.items.ControllableItem import ControllableItem


class ControlableSpaceTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._ctl = Controller()

    def test_controlableSpace(self):
        _cs = ControllableSpace(maxPopulation=10)
        for i in range(5):
            _cs.addControllable(ControllableItem(controllable=True, name=f'name_{i}',
                                                 parentController=self._ctl))

        self.assertEqual(len(_cs), 5)

    def test_controlable_exception(self):
        _cs = ControllableSpace(maxPopulation=10)
        try:
            for i in range(11):
                _cs.addControllable(ControllableItem(controllable=True, name=f'name_{i}',
                                                     parentController=self._ctl))
        except MaxControllableSpacePopulationException as e:
            self.assertEqual(MaxControllableSpacePopulationException, type(e))


if __name__ == '__main__':
    unittest.main()
