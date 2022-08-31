import logging
from typing import Dict, Type

from application import errors
from application import handlers as _handlers
from domain import commands, events


class App:
    def __init__(
        self,
        handlers: Dict[Type[commands.Command], _handlers.Handler],
        logger: logging.Logger,
    ):
        self.handlers = handlers
        self.logger = logger

    def handle(self, command: commands.Command) -> events.Event:
        if not type(command) in self.handlers:
            raise errors.HandlerNotFound

        handler = self.handlers[type(command)]

        try:
            return handler.handle(command)
        except Exception as e:
            self.logger.error(e)
            raise errors.HandlerError(str(e))
