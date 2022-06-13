from typing import Callable, Union

from .error_handlers import keys_exists
import re
import requests
#from queue import Queue


class Update:
    def __init__(self, update) -> None:
        self.value = update
        self.message = self.value["messages"][0]
        self.user = self.value["contacts"][0]
        self.user_display_name = self.user["profile"]["name"]
        self.user_phone_number = self.user["wa_id"]
        if keys_exists(self.message, "text", "body"):
            self.message_text = self.message["text"]["body"]


class Update_handler:
    def __init__(self) -> None:
        self.name = None
        self.regex = None
        self.func = None
        self.action = None

    def filter_check(self, msg) -> bool:
        if self.regex:
            if re.match(self.regex, msg):
                return True
            else:
                return False
        if self.func:
            if self.func(msg):
                return True
            else:
                return False

        return True

    def run(self, update):
        return self.action(update)


class Dispatcher:
    def __init__(self, bot, mark_as_read: bool = True) -> None:
        self.bot = bot
        self.registered_handlers = []  # list of handler instances
        self.mark_as_read = mark_as_read
        self.next_step_handler = {}
        self.fallback_function = None

    def process_update(self, update) -> None:
        if not keys_exists(update, "entry"):
            return
        value = update["entry"][0]["changes"][0]["value"]
        self.value = value
        if not keys_exists(value, "metadata", "phone_number_id"):
            return
        if value["metadata"]["phone_number_id"] == self.bot.id:
            if not keys_exists(value, "messages"):
                return
            self.message = value["messages"][0]
            if self.mark_as_read:
                self.bot.mark_as_read(self.message)
            print("regd hands", self.registered_handlers)
            print("regd nxts", self.next_step_handler)
            update = Update(value)
            try:
                users_next_step = self.next_step_handler[update.user_phone_number]
                users_next_step_handler = users_next_step['next_step_handler']
                matched_handlers = [users_next_step_handler]
                try:
                    users_next_step_fallback = users_next_step['fallback_function']
                    matched_handlers.append(users_next_step_fallback)
                except KeyError:
                    pass
            except KeyError:
                matched_handlers = [i for i in self.registered_handlers]  # if isinstance(
                # i, Update_handler) and i.name == self.message["type"]]
            for handler in matched_handlers:
                if isinstance(handler, Update_handler) and handler.name == self.message["type"]:
                    if self.message["type"] == "text" or self.message["type"] == "interactive":
                        message = self.message["text"]["body"]
                    res = self._check_and_run_handler(handler, message)
                    if res:
                        try:
                            if self.next_step_handler[update.user_phone_number]['next_step_handler'] == handler or self.next_step_handler[update.user_phone_number]['fallback_function'] == handler:
                                self.next_step_handler[update.user_phone_number] = {
                                }
                            return
                        except KeyError:
                            return

    def _check_and_run_handler(self, handler, message):
        if hasattr(handler, 'filter_check'):
            if not handler.filter_check(message):
                return False
            handler.run(Update(self.value))
            return True
        return False

    def add_handler(self, handler_instance):
        self.registered_handlers.append(handler_instance)
        handler_index = len(self.registered_handlers)-1
        return handler_index

    def set_next_handler(self, update: Update, handler_type: Update_handler, function: Callable, end_conversation_action: Callable = lambda x: x, end_conversation_keyword_regex: str = r"[eE][nN][dD]", **kwargs):
        """Sets a function for handling of next update. 
        The set handler overrides other handlers till it handles an update itself"""
        if not issubclass(handler_type, Update_handler):
            return "type should be an Update_handler class"
        try:
            regex = kwargs['regex']
        except KeyError:
            regex = None
        try:
            func = kwargs['func']
        except KeyError:
            func = None
        self.next_step_handler[update.user_phone_number] = {}
        users_next = self.next_step_handler[update.user_phone_number]
        users_next['fallback_function'] = Message_handler(
            regex=end_conversation_keyword_regex, action=end_conversation_action)
        if handler_type == Message_handler:
            users_next['next_step_handler'] = Message_handler(
                regex, func, function)
            print("reggin self'd", self.next_step_handler, self.fallback_function)

    def add_message_handler(self, regex: str = None, func: Callable = None):
        def inner(function):
            _handler = Message_handler(regex, func, function)
            return self.add_handler(_handler)
        return inner

    def interactive_handler(self):
        pass

    def location_handler(self):
        pass

    def media_handler(self):
        pass


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


class Interactive_query_handler(Update_handler):
    """For button_reply and list_reply"""

    def __init__(self) -> None:
        super().__init__()


class Media_handler(Update_handler):
    """Image, audio and video"""

    def __init__(self) -> None:
        super().__init__()
