import logging
from typing import Dict, Type

from application import handlers as _handlers
from domain import commands, events, queries


class App:
    def __init__(
        self,
        handlers: Dict[Type[commands.Command | queries.Query], _handlers.Handler],
        logger: logging.Logger,
    ):
        self.handlers = handlers
        self.logger = logger

    def handle(self, request: commands.Command | queries.Query) -> events.Event:
        if not type(request) in self.handlers:
            raise RuntimeError(f"Missing handler for {type(request)}")

        return self.handlers[type(request)].handle(request)
