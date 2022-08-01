from .dispatcher import Dispatcher, Update
from .message import (
    message_interactive, mark_as_read, message_text, message_template, message_location)
from .markup import Reply_markup
from typing import Union
from queue import Queue


class Whatsapp():
    def __init__(self, number_id: int, token: str, mark_as_read: bool = True) -> None:
        """This is the main Whatsapp class. Use it to initialize your bot
        Args:
            id: Your phone number id provided by WhatsApp cloud
            token : Your token provided by WhatsApp cloud
            mark_as_read:(bool), Use to set whether incoming messages should be marked as read. Default is True"""
        self.queue = Queue()
        self.threaded = True
        self.id = number_id
        self.token = token
        self.msg_url = f"https://graph.facebook.com/v13.0/{str(self.id)}/messages"
        self.dispatcher = Dispatcher(self, mark_as_read)
        self.on_message = self.dispatcher.add_message_handler
        self.on_interactive_message = self.dispatcher.add_interactive_handler
        self.set_next_step = self.dispatcher.set_next_handler

    def process_update(self, update):
        return self.dispatcher.process_update(update)

    def mark_as_read(self, update):
        """Mark any message as read"""
        return mark_as_read(update, self.msg_url, self.token)

    def reply_message(self, update: Update, text, reply_markup: Reply_markup = None, header: str = None, footer: str = None, web_page_preview=True):
        return self.send_message(
            update.user_phone_number, text, reply_markup, header, footer, web_page_preview=web_page_preview)

    def reply_template(self, update: Update, template_name: str):
        return self.send_template_message(
            update.user_phone_number, template_name)

    def send_message(self, phone_num: str, text: str, reply_markup: Reply_markup = None, header: str = None, footer: str = None, web_page_preview=True):
        """Sends text message
        Args:
            phone_num:(int) Recipeint's phone number
            text:(str) The text to be sent
            web_page_preview:(bool),optional. Turn web page preview of links on/off
        """
        if reply_markup:
            return message_interactive(self.msg_url, self.token, phone_num, text, reply_markup, header=header, footer=footer, web_page_preview=web_page_preview)
        else:
            return message_text(self.msg_url, self.token, phone_num, text, web_page_preview=web_page_preview)

    def send_template_message(self, phone_num: str, template_name: str):
        """Sends preregistered template message"""
        return message_template(self.msg_url, self.token, phone_num, template_name)
