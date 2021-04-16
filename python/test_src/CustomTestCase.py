import logging
import logging.config
import os
import aiounittest


class CustomTestCase(aiounittest.AsyncTestCase):
    def setUp(self) -> None:
        logging.config.fileConfig(fname=os.path.join(os.path.dirname(__file__), '..', 'config', 'logging_debug.conf'))
