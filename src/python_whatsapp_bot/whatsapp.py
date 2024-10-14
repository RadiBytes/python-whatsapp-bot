from .dispatcher import Dispatcher, Update
from .message import (
    download_media,
    get_media_url,
    message_interactive,
    mark_as_read,
    message_text,
    message_template,
    upload_media,
    message_media,
    message_location,
)
from .markup import Reply_markup
from typing import Union
from queue import Queue


class Whatsapp:

    def __init__(self, number_id: int, token: str, mark_as_read: bool = True) -> None:
        """This is the main Whatsapp class. Use it to initialize your bot
        Args:
            id: Your phone number id provided by WhatsApp cloud
            token : Your token provided by WhatsApp cloud
            mark_as_read:(bool), Use to set whether incoming messages should be marked as read. Default is True
        """
        self.version_number: int = 21
        self.queue = Queue()
        self.threaded = True
        self.id = number_id
        self.token = token
        self.base_url = f"https://graph.facebook.com/v{str(float(self.version_number))}"
        self.msg_url = self.base_url + f"/{str(self.id)}/messages"
        self.media_url = self.base_url + f"/{str(self.id)}/media"
        self.dispatcher = Dispatcher(self, mark_as_read)
        self.on_message = self.dispatcher.add_message_handler
        self.on_interactive_message = self.dispatcher.add_interactive_handler
        self.on_image_message = self.dispatcher.add_image_handler
        self.on_audio_message = self.dispatcher.add_audio_handler
        self.on_video_message = self.dispatcher.add_video_handler
        self.on_sticker_message = self.dispatcher.add_sticker_handler
        self.on_location_message = self.dispatcher.add_location_handler
        self.set_next_step = self.dispatcher.set_next_handler

    def _set_base_url(self):
        self.base_url = f"https://graph.facebook.com/v{str(float(self.version_number))}"

    def set_version(self, version_number: int):
        self.version_number = version_number
        self._set_base_url()

    def process_update(self, update):
        return self.dispatcher.process_update(update)

    def mark_as_read(self, update):
        """Mark any message as read"""
        return mark_as_read(update, self.msg_url, self.token)

    def reply_message(
        self,
        phone_num: str,
        text: str,
        msg_id: str = "",
        reply_markup: Reply_markup = None,
        header: str = None,
        header_type: str = "text",
        footer: str = None,
        web_page_preview=True,
        tag_message: bool = True,
    ):
        return self.send_message(
            phone_num,
            text,
            msg_id,
            reply_markup,
            header,
            header_type,
            footer,
            web_page_preview=web_page_preview,
            tag_message=tag_message,
        )

    def reply_template(self, update: Update, template_name: str):
        return self.send_template_message(update.user_phone_number, template_name)

    def reply_media(
        self,
        update: Update,
        image_path: str,
        caption: str = None,
        media_provider_token: str = None,
    ):
        return self.send_media_message(
            update.user_phone_number, image_path, caption, media_provider_token
        )

    def send_message(
        self,
        phone_num: str,
        text: str,
        msg_id: str = "",
        reply_markup: Reply_markup = None,
        header: str = None,
        header_type: str = "text",
        footer: str = None,
        web_page_preview=True,
        tag_message: bool = True,
    ):
        """Sends text message
        Args:
            phone_num:(int) Recipeint's phone number
            text:(str) The text to be sent
            web_page_preview:(bool),optional. Turn web page preview of links on/off
        """
        if reply_markup:
            return message_interactive(
                self.msg_url,
                self.token,
                phone_num,
                text,
                reply_markup,
                msg_id=msg_id,
                header=header,
                header_type=header_type,
                footer=footer,
                web_page_preview=web_page_preview,
            )
        else:
            return message_text(
                self.msg_url,
                self.token,
                phone_num,
                text,
                msg_id=msg_id,
                web_page_preview=web_page_preview,
                tag_message=tag_message,
            )

    def send_template_message(
        self,
        phone_num: str,
        template_name: str,
        components: list = None,
        language_code: str = None,
    ):
        """Sends preregistered template message"""
        return message_template(
            self.msg_url,
            self.token,
            phone_num,
            template_name,
            components,
            language_code,
        )

    def upload_media(
        self,
    ):
        return upload_media(self.media_url, self.token)

    def get_media_url(self, media_id: str):
        return get_media_url(self.base_url, media_id, self.token).json()

    def download_media(self, media_id: str, file_path: str):
        return download_media(self.base_url, media_id, self.token, file_path)

    def send_media_message(
        self,
        phone_num: str,
        image_path: str,
        caption: str = None,
        media_provider_token: str = None,
    ):
        """Sends media message which may include audio, document, image, sticker, or video
        Using media link or by uploading media from file.
        paths starting with http(s):// or www. will be treated as link, others will be treated as local files
        """
        return message_media(
            self.msg_url,
            self.token,
            phone_num,
            image_path,
            caption,
            media_provider_token,
        )
