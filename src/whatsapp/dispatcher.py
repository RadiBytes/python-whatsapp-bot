from typing import Callable, Union

from whatsapp_cloud.src.whatsapp import message
from .error_handlers import keys_exists
import re
import requests


class Dispatcher:
    def __init__(self, bot, mark_as_read: bool = True) -> None:
        self.bot = bot
        self.registered_handlers = []  # list of handler instances
        self.mark_as_read = mark_as_read

    def process_update(self, update) -> None:
        if not keys_exists(update, "entry"):
            return
        value = update["entry"][0]["changes"][0]["value"]
        if not keys_exists(value, "metadata", "phone_number_id"):
            return
        if value["metadata"]["phone_number_id"] == self.bot.id:
            if not keys_exists(value, "messages"):
                return
            self.message = value["messages"][0]
            print("slf msg", self.message)
            if self.mark_as_read:
                self.bot.mark_as_read(self.message)
            print(self.registered_handlers)
            matched_handlers = [i for i in self.registered_handlers if isinstance(
                i, Update_handler) and i.name == self.message["type"]]
            for handler in matched_handlers:
                if self.message["type"] == "text":
                    message = self.message["text"]["body"]
                elif self.message["type"] == "interactive":
                    message = self.message["text"]["body"]
                res = self._handler_check(handler, message)
                if res:
                    return

    def _handler_check(self, handler, message):

        if hasattr(handler, 'filter_check'):
            if not handler.filter_check(message):
                return False
            print("passed filtering")
            handler.run(self.message)
            return True
        return False

    def add_handler(self, handler_instance):
        print("addn hndlr msgn")
        self.registered_handlers.append(handler_instance)
        handler_index = len(self.registered_handlers)-1
        return handler_index

    def message_handler(self, regex: str = None, func: Callable = None):
        def inner(function):
            _handler = Message_handler(regex, func, function)
            return self.add_handler(_handler)
        return inner

    def interactive_handler(self):
        pass

    def conversation_handler(self, conv_start: Callable, fallback: Callable = None):
        def decorator(function):
            def wrapper(update):
                _handler = Conversation_handler(
                    'regex', 'func', function)  # Fix from here------------
                return self.add_handler(_handler)
            return wrapper
        return decorator

    def location_handler(self):
        pass

    def media_handler(self):
        pass


class Update_handler:
    def __init__(self) -> None:
        self.name = None
        self.regex = None
        self.func = None
        self.temp_filter = None

    def filter_check(self, msg) -> bool:
        if self.regex:
            print("filtering", msg)
            if re.match(self.regex, msg):
                print("filtering 2222", msg)
                return True
        if self.func:
            print("filtering funccc", msg)
            if self.func(msg):
                print("filtering funccc22222", msg)
                return True

        return False

    def run(self, update):
        return self.action(update)

    def mark_as_read(self, update):
        q = {"messaging_product": "whatsapp",
             "status": "read",
             "message_id": "MESSAGE_ID"
             }


class Message_handler(Update_handler):
    def __init__(self, regex: str = None, func: Callable = None, action: Callable = None) -> None:
        super().__init__()
        self.name = "text"
        self.regex = regex
        self.func = func
        self.action = action


class Location_handler(Update_handler):
    def __init__(self) -> None:
        super().__init__()


class Conversation_handler(Update_handler):
    def __init__(self, conv_start: Callable, fallback: Callable = None) -> None:
        super().__init__()
        self.conv_start = conv_start
        self.fallback = fallback


class Interactive_query_handler(Update_handler):
    """For button_reply and list_reply"""

    def __init__(self) -> None:
        super().__init__()


class Media_handler(Update_handler):
    def __init__(self) -> None:
        super().__init__()
