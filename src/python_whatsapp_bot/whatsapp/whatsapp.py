from .dispatcher import Dispatcher, Update
from .message import (
    message_interactive, mark_as_read, message_text, message_template, upload_media, message_media, message_location)
from .markup import Reply_markup
from typing import Union
from queue import Queue


class Whatsapp():
    version_number = 14

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
        self.base_url = f"https://graph.facebook.com/v{str(float(self.version_number))}/{str(self.id)}"
        self.msg_url = self.base_url+"/messages"
        self.media_url = self.base_url+'/media'
        self.dispatcher = Dispatcher(self, mark_as_read)
        self.on_message = self.dispatcher.add_message_handler
        self.on_interactive_message = self.dispatcher.add_interactive_handler
        self.set_next_step = self.dispatcher.set_next_handler

    def process_update(self, update):
        return self.dispatcher.process_update(update)

    def mark_as_read(self, update):
        """Mark any message as read"""
        return mark_as_read(update, self.msg_url, self.token)

    def reply_message(self, update: Update, text, reply_markup: Reply_markup = None, header: str = None, header_type: str = "text", footer: str = None, web_page_preview=True):
        return self.send_message(
            update.user_phone_number, text, reply_markup, header, header_type, footer, web_page_preview=web_page_preview)

    def reply_template(self, update: Update, template_name: str):
        return self.send_template_message(
            update.user_phone_number, template_name)

    def reply_media(self, update: Update, image_path: str, caption: str = None, media_provider_token: str = None):
        return self.send_media_message(
            update.user_phone_number, image_path, caption, media_provider_token)

    def send_message(self, phone_num: str, text: str, reply_markup: Reply_markup = None, header: str = None, header_type: str = "text", footer: str = None, web_page_preview=True):
        """Sends text message
        Args:
            phone_num:(int) Recipeint's phone number
            text:(str) The text to be sent
            web_page_preview:(bool),optional. Turn web page preview of links on/off
        """
        if reply_markup:
            return message_interactive(self.msg_url, self.token, phone_num, text, reply_markup, header=header, header_type=header_type, footer=footer, web_page_preview=web_page_preview)
        else:
            return message_text(self.msg_url, self.token, phone_num, text, web_page_preview=web_page_preview)

    def send_template_message(self, phone_num: str, template_name: str):
        """Sends preregistered template message"""
        return message_template(self.msg_url, self.token, phone_num, template_name)

    def upload_media(self,):

        return upload_media(self.media_url)

    def send_media_message(self, phone_num: str, image_path: str, caption: str = None, media_provider_token: str = None):
        """Sends media message which may include audio, document, image, sticker, or video 
        Using media link or by uploading media from file.
        paths starting with http(s):// or www. will be treated as link, others will be treated as local files """
        return message_media(self.msg_url, self.token, phone_num, image_path, caption, media_provider_token)
