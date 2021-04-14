import unittest
from controller.Controller import Controller
from controller.PriorityControl import PriorityControl


class MyTestCase(unittest.TestCase):
    def test_controller_length(self):
        controller = Controller()
        controller.addController(priorityController=PriorityControl(priority=10))
        controller.addController(priorityController=PriorityControl(priority=20))
        controller.addController(priorityController=PriorityControl(priority=30))

        self.assertEqual(len(controller), 3)


if __name__ == '__main__':
    unittest.main()
