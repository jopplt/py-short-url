import logging
from typing import Dict, Type, Union

from application import errors
from application import handlers as _handlers
from domain import commands, events, queries


class App:
    def __init__(
        self,
        handlers: Dict[
            Type[Union[commands.Command | queries.Query]], _handlers.Handler
        ],
        logger: logging.Logger,
    ):
        self.handlers = handlers
        self.logger = logger

    def handle(self, request: Union[commands.Command, queries.Query]) -> events.Event:
        if not type(request) in self.handlers:
            raise errors.HandlerNotFound

        handler = self.handlers[type(request)]

        try:
            return handler.handle(request)
        except Exception as e:
            self.logger.error(e)
            raise errors.HandlerError(str(e))
