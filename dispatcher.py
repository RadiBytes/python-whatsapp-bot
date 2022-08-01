import inspect
from typing import Callable, Union
from .markup import Reply_markup
from .error_handlers import keys_exists
import re
import requests
from .user_context import User_context
#from queue import Queue
from threading import Thread


class Update:
    def __init__(self, bot, update) -> None:
        self.bot = bot
        self.value = update
        try:
            self.message = self.value["messages"][0]
        except:
            self.message = {}
        self.user = self.value["contacts"][0]
        self.user_display_name = self.user["profile"]["name"]
        self.user_phone_number = self.user["wa_id"]
        self.message_text = None
        #self.list_text = None
        self.interactive_text = None
        if keys_exists(self.message, "text", "body"):
            self.message_text = self.message["text"]["body"]
        if keys_exists(self.message, "interactive", "list_reply"):
            self.interactive_text = self.message["interactive"]["list_reply"]
            self.message_text = self.message["interactive"]["list_reply"]['id']
        if keys_exists(self.message, "interactive", "button_reply"):
            self.interactive_text = self.message["interactive"]["button_reply"]
            self.message_text = self.message["interactive"]["button_reply"]['id']

    def reply_message(self, text: str, reply_markup: Reply_markup = None, header: str = None, footer: str = None, web_page_preview=True, *args, **kwargs):
        self.bot.send_message(self.user_phone_number, text, reply_markup=reply_markup,
                              header=header, footer=footer, web_page_preview=web_page_preview, *args, **kwargs)


class Update_handler:
    def __init__(self, context: bool = True) -> None:
        self.name = None
        self.regex = None
        self.func = None
        self.action = None
        self.context = context
        self.list = None
        self.button = None

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

    def run(self, *args, **kwargs):
        new_kwargs = {
            i: kwargs[i] for i in kwargs if i in inspect.getfullargspec(self.action).args}
        return self.action(*args, **new_kwargs)


class Message_handler(Update_handler):
    def __init__(self, regex: str = None, func: Callable = None, action: Callable = None, context: bool = True) -> None:
        super().__init__(context)
        self.name = "text"
        self.regex = regex
        self.func = func
        self.action = action


class Interactive_query_handler(Update_handler):
    """For button_reply and list_reply"""

    def __init__(self, regex: str = None, func: Callable = None, handle_button: bool = True, handle_list: bool = True, action: Callable = None, context: bool = True) -> None:
        super().__init__(context)
        self.name = "interactive"
        self.regex = regex
        self.func = func
        self.action = action
        self.list = handle_list
        self.button = handle_button


class Location_handler(Update_handler):
    def __init__(self) -> None:
        super().__init__()


class Media_handler(Update_handler):
    """Image, audio and video"""

    def __init__(self) -> None:
        super().__init__()


class Dispatcher:
    def __init__(self, bot, mark_as_read: bool = True) -> None:
        self.bot = bot
        self.queue = bot.queue
        self.registered_handlers = []  # list of handler instances
        self.mark_as_read = mark_as_read
        self.next_step_handler = {}
        self.fallback_function = None

    def process_update(self, update) -> None:
        # ------------new---------
        # self._process_queue(update)
        # ------------old3--------
        # Thread(target=self._process_queue(update)).start()

        # -----------old2------
        # if not self.bot.threaded:
        #     self._process_queue(update)
        # else:
        #     Thread(target=self._process_queue(update)).start()

        # ---------------old------
        self.queue.put(update)
        while True:
            _update = self.queue.get()
            if not self.bot.threaded:
                self._process_queue(_update)
            else:
                Thread(target=self._process_queue(_update)).start()
            if self.queue.empty():
                print("finished q")
                break

    def _process_queue(self, update) -> None:
        if not keys_exists(update, "entry", 0, "changes", 0, "value"):
            return
        value = update["entry"][0]["changes"][0]["value"]
        #self.value = value
        if not keys_exists(value, "metadata", "phone_number_id"):
            return
        if value["metadata"]["phone_number_id"] == self.bot.id:
            if not keys_exists(value, "messages"):
                return
            _message = value["messages"][0]
            if self.mark_as_read:
                self.bot.mark_as_read(_message)
            update = Update(self.bot, value)
            print(update.message)

            # check if a next step handler has been registered
            try:
                users_next_step = self.next_step_handler[update.user_phone_number]
                users_next_step_handler = users_next_step['next_step_handler']
                matched_handlers = []
                try:
                    users_next_step_fallback = users_next_step['fallback_function']
                    matched_handlers.append(users_next_step_fallback)
                except KeyError:
                    pass
                matched_handlers.append(users_next_step_handler)
            # get registered handlers if no next step handler
            except KeyError:
                matched_handlers = [i for i in self.registered_handlers]
            for handler in matched_handlers:
                if isinstance(handler, Update_handler) and handler.name == _message["type"]:

                    # handle text
                    if _message["type"] == "text":
                        message_txt = _message["text"]["body"]

                    # handle interactive
                    elif _message["type"] == "interactive":
                        if _message["interactive"]["type"] == 'button_reply' and handler.button:
                            message_txt = _message["interactive"]['button_reply']['id']
                        elif _message["interactive"]["type"] == 'list_reply' and handler.list:
                            message_txt = _message["interactive"]['list_reply']['id']
                        else:
                            return
                    res = self._check_and_run_handler(
                        handler, value, message_txt)
                    if res:
                        try:
                            if self.next_step_handler[update.user_phone_number]['next_step_handler'] == handler or self.next_step_handler[update.user_phone_number]['fallback_function'] == handler:
                                del self.next_step_handler[update.user_phone_number]
                            return
                        except KeyError:
                            return

    def _check_and_run_handler(self, handler, value, message):
        if hasattr(handler, 'filter_check'):
            if not handler.filter_check(message):
                return False
            if handler.context:
                update = Update(self.bot, value)
                handler.run(update, context=User_context(
                    update.user_phone_number))
            else:
                handler.run(update)
            return True
        return False

    def add_handler(self, handler_instance):
        self.registered_handlers.append(handler_instance)
        handler_index = len(self.registered_handlers)-1
        return handler_index

    def set_next_handler(self, update: Update, function: Callable, handler_type: Update_handler = Message_handler, regex: str = None, func: Callable = None, end_conversation_action: Callable = lambda x: x, end_conversation_keyword_regex: str = r"(?i)^(end|stop|cancel)$"):
        """Sets a function for handling of next update. 
        The set_next_handler overrides other handlers till it handles an update itself"""
        if not issubclass(handler_type, Update_handler):
            return "type should be an Update_handler class"
        regex = regex
        func = func
        self.next_step_handler[update.user_phone_number] = {}
        users_next = self.next_step_handler[update.user_phone_number]
        users_next['fallback_function'] = Message_handler(
            regex=end_conversation_keyword_regex, action=end_conversation_action)
        if handler_type == Message_handler:
            users_next['next_step_handler'] = Message_handler(
                regex, func, action=function)
        if handler_type == Interactive_query_handler:
            users_next['next_step_handler'] = Interactive_query_handler(
                regex, func, action=function)

    def add_message_handler(self, regex: str = None, func: Callable = None, context: bool = True):
        def inner(function):
            _handler = Message_handler(
                regex=regex, func=func, action=function, context=context)
            self.add_handler(_handler)
            return function
        return inner

    def add_interactive_handler(self, regex: str = None, func: Callable = None, handle_button: bool = True, handle_list: bool = True, action: Callable = None, context: bool = True):
        def inner(function):
            _handler = Interactive_query_handler(
                regex=regex, func=func, action=function, handle_button=handle_button, handle_list=handle_list, context=context)
            self.add_handler(_handler)
            return function
        return inner

    def location_handler(self):
        pass

    def media_handler(self):
        pass
