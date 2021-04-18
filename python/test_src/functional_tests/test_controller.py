import asyncio
import logging
import aiounittest

from controller.ControllableSpace import ControllableSpace
from controller.Controller import Controller
from controller.ControllerWatcher import ControllerWatcher
from controller.exceptions import MaxControllableSpacePopulationException
from core.items.ControllableItem import ControllableItem
from core.location.ObjectLocation import Location, ObjectLocation
from python.test_src.CustomTestCase import CustomTestCase


class ControllerTestCase(CustomTestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _latitude = Location(degree=40, minute=42, second=51, locationType=Location.LATITUDE)
        _longitude = Location(degree=-74, minute=0, second=21, locationType=Location.LONGITUDE)
        self._nyc = ObjectLocation(longitude=_longitude, latitude=_latitude, height=0)

    @staticmethod
    async def stop_controller(controller: Controller):
        await asyncio.sleep(10)
        logging.info('Starting to stop controller')
        await controller.stop()

    async def test_controller(self):
        _ctl = Controller()
        _ctlSpace = ControllableSpace(name='test', maxPopulation=50)
        _ctl.addControllableSpace(_ctlSpace)
        _ctlTask = asyncio.ensure_future(_ctl.start())
        _stopCtlTask = asyncio.ensure_future(ControllerTestCase.stop_controller(controller=_ctl))
        _watchCtl = asyncio.ensure_future(ControllerWatcher(sleepInterval=1.0, controller=_ctl).start())

        await _ctlTask
        await _stopCtlTask
        try:
            await _watchCtl
        except Exception as e:
            logging.exception(e)
        logging.info('Test completed')

        self.assertEqual(_ctl.controllerStop, True)

    async def test_controller_add_population(self):
        _ctl = Controller()
        _ctlSpace = ControllableSpace(name='test', maxPopulation=50)
        _ctl.addControllableSpace(_ctlSpace)
        _ctlTask = asyncio.ensure_future(_ctl.start())
        _stopCtlTask = asyncio.ensure_future(ControllerTestCase.stop_controller(controller=_ctl))
        _watchCtl = asyncio.ensure_future(ControllerWatcher(sleepInterval=1.0, controller=_ctl).start())

        async def addControllableItems(howMany: int = 10):
            tries = 0
            while True:
                logging.info(f'Adding {howMany} items')
                for _i in range(howMany):
                    _ctl.addControllableItem(ControllableItem(objectLocation=self._nyc,
                                                              controllable=True,
                                                              name=f'name_{_i}_{tries}',
                                                              parentController=_ctl,
                                                              ),
                                             ctlSpace=_ctlSpace.name)
                tries += 1
                await asyncio.sleep(1.0)

        _addCtlTask = asyncio.ensure_future(addControllableItems())

        await _ctlTask
        await _stopCtlTask
        try:
            await _watchCtl
        except Exception as e:
            logging.exception(e)

        try:
            await _addCtlTask
        except MaxControllableSpacePopulationException as e:
            logging.exception(e)

        logging.info('Test completed')

        self.assertEqual(50, _ctl.getControllablePopulation('test'))
        self.assertEqual(_ctl.controllerStop, True)

    async def test_controller_remove_population(self):
        _ctl = Controller()
        _ctlSpace = ControllableSpace(name='test', maxPopulation=50)
        _ctl.addControllableSpace(_ctlSpace)
        _ctlTask = asyncio.ensure_future(_ctl.start())
        _stopCtlTask = asyncio.ensure_future(ControllerTestCase.stop_controller(controller=_ctl))
        _watchCtl = asyncio.ensure_future(ControllerWatcher(sleepInterval=1.0, controller=_ctl).start())

        async def addControllableItems(howMany: int = 10):
            tries = 0
            while True:
                logging.info(f'Adding {howMany} items')
                for _i in range(howMany):
                    _ctl.addControllableItem(ControllableItem(objectLocation=self._nyc,
                                                              controllable=True,
                                                              name=f'name_{_i}_{tries}',
                                                              parentController=_ctl),
                                             ctlSpace=_ctlSpace.name
                                             )
                    await asyncio.sleep(0.2)
                tries += 1
                await asyncio.sleep(1.0)

        async def removeControllableItems(howMany: int = 10):
            tries = 0

            await asyncio.sleep(5.0)
            logging.info(f'Removing {howMany} items')
            for _i in range(howMany):
                _ctl.removeControllableItem(name=f'name_{_i}_{tries}', ctlSpace='test')
            await asyncio.sleep(3.0)

        _addCtlTask = asyncio.ensure_future(addControllableItems())
        _delCtlTask = asyncio.ensure_future(removeControllableItems())

        await _ctlTask
        await _stopCtlTask
        try:
            await _watchCtl
        except Exception as e:
            logging.exception(e)

        try:
            await _addCtlTask
        except MaxControllableSpacePopulationException as e:
            logging.exception(e)

        try:
            _delCtlTask.cancel()
        except Exception as e:
            logging.exception(e)

        logging.info('Test completed')

        self.assertEqual(50, _ctl.getControllablePopulation('test'))
        self.assertEqual(_ctl.controllerStop, True)


if __name__ == '__main__':
    aiounittest.main()
