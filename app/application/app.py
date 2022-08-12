import logging
from typing import Dict, Type

from application.errors import HandlerError
from application.handlers import Handler
from domain import commands, events


class App:
    def __init__(
        self, handlers: Dict[Type[commands.Command], Handler], logger: logging.Logger
    ):
        self.handlers = handlers
        self.logger = logger

    def handle(self, command: commands.Command) -> events.Event:
        try:
            handler = self.handlers[type(command)]
            return handler.handle(command)
        except Exception as e:
            self.logger.error(e)
            raise HandlerError(str(e))
