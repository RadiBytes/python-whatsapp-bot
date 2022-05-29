from .message import (
    message_interactive, message_text, message_location)
from .markup import Reply_markup
from typing import Union


class Whatsapp():
    def __init__(self, _id: int, token: str) -> None:
        self.id = _id
        self.token = token
        self.msg_url = f"https://graph.facebook.com/v13.0/{str(self.id)}/messages"

    def send_text_message(self, phone_num: int, text: str, web_page_preview=True):
        """Sends text message
        Args:
            phone_num:(int) Recipeint's phone number
            text:(str) The text to be sent
            web_page_preview:(bool),optional. Turn web page preview of links on/off
        """
        return message_text(self.msg_url, self.token, phone_num, text, web_page_preview=web_page_preview)

    def send_interactive_message(self, phone_num: int, text: str, reply_markup: Reply_markup, header: str = None, footer: str = None, web_page_preview=True):
        """Sends text message
        Args:
            phone_num:(int) Recipeint's phone number
            text:(str) The text to be sent
            web_page_preview:(bool),optional. Turn web page preview of links on/off
            reply_keyboard_markup:(Reply_keyboard),optional. A keyboard markup object to be sent with the text
        """
        return message_interactive(self.msg_url, self.token, phone_num, str, reply_markup, header=header, footer=footer, web_page_preview=web_page_preview)
