from .dispatcher import Dispatcher, Update
from .message import (
    message_interactive, mark_as_read, message_text, message_location)
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
        self.add_message_handler = self.dispatcher.add_message_handler
        self.set_next_step_handler = self.dispatcher.set_next_handler

    def process_update(self, update):
        return self.dispatcher.process_update(update)

    def mark_as_read(self, update):
        """Mark any message as read"""
        return mark_as_read(update, self.msg_url, self.token)

    def reply_text(self, update: Update, text, web_page_preview=True):
        return self.send_text_message(
            update.user_phone_number, text, web_page_preview=web_page_preview)

    def send_text_message(self, phone_num: str, text: str, web_page_preview=True):
        """Sends text message
        Args:
            phone_num:(int) Recipeint's phone number
            text:(str) The text to be sent
            web_page_preview:(bool),optional. Turn web page preview of links on/off
        """
        return message_text(self.msg_url, self.token, phone_num, text, web_page_preview=web_page_preview)

    def send_interactive_message(self, phone_num: str, text: str, reply_markup: Reply_markup, header: str = None, footer: str = None, web_page_preview=True):
        """Sends text message
        Args:
            phone_num:(int) Recipeint's phone number
            text:(str) The text to be sent
            web_page_preview:(bool),optional. Turn web page preview of links on/off
            reply_keyboard_markup:(Reply_keyboard),optional. A keyboard markup object to be sent with the text
        """
        return message_interactive(self.msg_url, self.token, phone_num, text, reply_markup, header=header, footer=footer, web_page_preview=web_page_preview)

    def reply_interactive(self, update: Update, text: str, reply_markup: Reply_markup, header: str = None, footer: str = None, web_page_preview=True):
        """Sends text message
        Args:
            phone_num:(int) Recipeint's phone number
            text:(str) The text to be sent
            web_page_preview:(bool),optional. Turn web page preview of links on/off
            reply_keyboard_markup:(Reply_keyboard),optional. A keyboard markup object to be sent with the text
        """
        return self.send_interactive_message(update.user_phone_number, text, reply_markup, header=header, footer=footer, web_page_preview=web_page_preview)
