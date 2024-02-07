import json
import logging
import os

from typing import Any
from logging import StreamHandler, FileHandler
from datetime import datetime

from models import settings

class Base:
    LOG_DIR: str = "./tmp/log"

    def __init__(self, event: Any, context: Any) -> None:
        self.event = event
        self.context = context
        settings.load_config(f"config/{os.environ.get('ENVIRONMENT', 'development')}.yaml")
        self.logger = self.__initialize_log()

        self.logger.info(event)

    def __initialize_log(self) -> logging.Logger:
        logger = logging.getLogger(__name__)
        log_level = os.environ.get("LOG_LEVEL", "DEBUG")
        logger.setLevel(log_level)

        handler = None
        if os.environ.get("AWS_LAMBDA_FUNCTION_NAME"):
            handler = StreamHandler()
        else:
            if not os.path.isdir(self.LOG_DIR):
                os.makedirs(self.LOG_DIR, exist_ok=True)

            log_filename = f"{self.LOG_DIR}/{datetime.now():%Y%m%d}.log"
            handler = FileHandler(log_filename)  # type: ignore

        handler.setFormatter(  # type: ignore
            logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
        )
        logger.addHandler(handler)  # type: ignore

        return logger
