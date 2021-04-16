import asyncio
import logging
import aiounittest

from controller.Controller import Controller, ControllerWatcher
from controller.exceptions import ControllerStoppedException, MaxControlableSpacePopulationException
from core.items.ControlableItem import ControlableItem
from python.test_src.CustomTestCase import CustomTestCase


class ControllerTestCase(CustomTestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    async def stop_controller(controller: Controller):
        await asyncio.sleep(10)
        logging.info('Starting to stop controller')
        await controller.stop()

    async def test_controller(self):
        _ctl = Controller()
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
        _ctlTask = asyncio.ensure_future(_ctl.start())
        _stopCtlTask = asyncio.ensure_future(ControllerTestCase.stop_controller(controller=_ctl))
        _watchCtl = asyncio.ensure_future(ControllerWatcher(sleepInterval=1.0, controller=_ctl).start())

        async def addControlableItems(howMany: int=10):
            tries = 0
            while True:
                logging.info(f'Adding {howMany} items')
                for _i in range(howMany):
                    _ctl.addControlableItem(ControlableItem(controllable=True,
                                                            name=f'name_{_i}_{tries}',
                                                            parentController=_ctl))
                tries += 1
                await asyncio.sleep(1.0)

        _addCtlTask = asyncio.ensure_future(addControlableItems())

        await _ctlTask
        await _stopCtlTask
        try:
            await _watchCtl
        except Exception as e:
            logging.exception(e)

        try:
            await _addCtlTask
        except MaxControlableSpacePopulationException as e:
            logging.exception(e)

        logging.info('Test completed')

        self.assertEqual(50, _ctl.getControllablePopulation())
        self.assertEqual(_ctl.controllerStop, True)

    async def test_controller_remove_population(self):
        _ctl = Controller()
        _ctlTask = asyncio.ensure_future(_ctl.start())
        _stopCtlTask = asyncio.ensure_future(ControllerTestCase.stop_controller(controller=_ctl))
        _watchCtl = asyncio.ensure_future(ControllerWatcher(sleepInterval=1.0, controller=_ctl).start())

        async def addControlableItems(howMany: int=10):
            tries = 0
            while True:
                logging.info(f'Adding {howMany} items')
                for _i in range(howMany):
                    _ctl.addControlableItem(ControlableItem(controllable=True,
                                                            name=f'name_{_i}_{tries}',
                                                            parentController=_ctl))
                tries += 1
                await asyncio.sleep(1.0)

        async def removeControlableItems(howMany: int=10):
            tries = 0

            await asyncio.sleep(5.0)
            logging.info(f'Removing {howMany} items')
            for _i in range(howMany):
                _ctl.removeControlableItem(name=f'name_{_i}_{tries}')
            await asyncio.sleep(3.0)

        _addCtlTask = asyncio.ensure_future(addControlableItems())
        _delCtlTask = asyncio.ensure_future(removeControlableItems())

        await _ctlTask
        await _stopCtlTask
        try:
            await _watchCtl
        except Exception as e:
            logging.exception(e)

        try:
            await _addCtlTask
        except MaxControlableSpacePopulationException as e:
            logging.exception(e)

        try:
            _delCtlTask.cancel()
        except Exception as e:
            logging.exception(e)

        logging.info('Test completed')

        self.assertEqual(50, _ctl.getControllablePopulation())
        self.assertEqual(_ctl.controllerStop, True)


if __name__ == '__main__':
    aiounittest.main()
