from typing import Union
from whatsapp.error_handlers import keys_exists
import re


class Dispatcher:
    # imported here to avoid circular import
    from whatsapp.whatsapp import Whatsapp

    def __init__(self, bot: Whatsapp) -> None:
        self.bot = bot
        self.registered_handlers = []  # list of handler instances
        pass

    def process_update(self, update) -> None:
        keys_exists(update, "entry")
        value = update["entry"][0]["changes"][0]["value"]
        keys_exists(value, "metadata", "phone_number_id")
        if value["metadata"]["phone_number_id"] == self.bot.id:
            keys_exists(value, "messages")
            self.message = value["messages"][0]
            matched_handlers = [i for i in self.registered_handlers if isinstance(
                i, Update_handler) and i.name == self.message["type"]]
            for handler in matched_handlers:
                res = self._handler_check(handler, self.message, self.message)
                if res:
                    return

    def _handler_check(self, handler, message):
        handle_instance = handler(message)
        if hasattr(handle_instance, 'filter_check'):
            if not handle_instance.filter_check(message):
                return False
        else:
            handle_instance.run(message)
            return True
        return False

    def add_handler(self, handler_instance):
        self.registered_handlers.append(handler_instance)
        handler_index = len(self.registered_handlers)-1
        return handler_index

    def message_handler(self, regex: str = None, func: function = None):
        def decorator(function):
            def wrapper(update):
                _handler = Message_handler(regex, func, function)
                return self.add_handler(_handler)
            return wrapper
        return decorator

    def interactive_handler(self):
        pass

    def conversation_handler(self, conv_start: function, fallback: function = None):
        def decorator(function):
            def wrapper(update):
                _handler = Conversation_handler(regex, func, function)
                return self.add_handler(_handler)
            return wrapper
        return decorator

    def location_handler(self):
        pass

    def media_handler(self):
        pass


class Update_handler:
    def __init__(self) -> None:
        self.regex = None
        self.func = None
        self.filter_list = None

    def filter_check(self, msg) -> bool:
        if self.regex:
            if re.match(self.regex, msg):
                return True
        if self.func:
            if self.func(msg):
                return True
        if self.filter_list:
            _filter_list = [i for i in self.filter_list]
            self.filter_list = None
            for i in _filter_list:
                if self.filter_check(i) == True:
                    return True
        return False

    def run(self, update):
        return self.action(update)


class Message_handler(Update_handler):
    def __init__(self, regex: str = None, func: function = None, filter_list: list[Union[str, function]] = None, action: function = None) -> None:
        super().__init__()
        self.regex = regex
        self.func = func
        self.action = action
        self.filter_list = filter_list


class Location_handler(Update_handler):
    def __init__(self) -> None:
        super().__init__()


class Conversation_handler(Update_handler):
    def __init__(self, conv_start: function, fallback: function = None) -> None:
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
