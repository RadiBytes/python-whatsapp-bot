import re
import inspect
from typing import Callable, Dict

from .markup import Reply_markup
from .error_handlers import keys_exists


class Update:

    def __init__(self, bot, update) -> None:
        self.bot = bot
        self.value = update
        self.message = self.value.get("messages", [{}])[0]
        self.user = self.value.get("contacts", [{}])[0]
        self.user_display_name: str = self.user.get("profile", {}).get("name", "")
        self.user_phone_number = self.user.get("wa_id", "")
        self.message_id: str = self.message.get("id")
        self.message_text: str = None
        self.interactive_text: str = None
        self.media_url: str = None
        self.media_mime_type: str = None
        self.media_file_id: str = None
        self.media_hash: str = None
        self.media_voice: bool = False
        self.loc_address: str = None
        self.loc_name: str = None
        self.loc_latitude: str = None
        self.loc_longitude: str = None

    #     self._initialize_message_text()

    # def _initialize_message_text(self):
    #     if keys_exists(self.message, "text", "body"):
    #         self.message_text = self.message["text"]["body"]
    #     if keys_exists(self.message, "interactive", "list_reply"):
    #         self.interactive_text = self.message["interactive"]["list_reply"]
    #         self.message_text = self.message["interactive"]["list_reply"]["id"]
    #     if keys_exists(self.message, "interactive", "button_reply"):
    #         self.interactive_text = self.message["interactive"]["button_reply"]
    #         self.message_text = self.message["interactive"]["button_reply"]["id"]

    def set_message_text(self, text: str):
        self.message_text = text

    def reply_message(
        self,
        text: str,
        reply_markup: Reply_markup = None,
        header: str = None,
        header_type: str = "text",
        footer: str = None,
        web_page_preview: bool = True,
        tag_message: bool = True,
        *args,
        **kwargs,
    ):
        return self.bot.reply_message(
            self.user_phone_number,
            text,
            msg_id=self.message_id,
            reply_markup=reply_markup,
            header=header,
            header_type=header_type,
            footer=footer,
            web_page_preview=web_page_preview,
            tag_message=tag_message,
            *args,
            **kwargs,
        )

    def reply_media(
        self,
        media_path,
        caption: str = None,
        media_provider_token: str = None,
        *args,
        **kwargs,
    ):
        return self.bot.reply_media(
            self.user_phone_number,
            media_path,
            caption,
            media_provider_token,
            *args,
            **kwargs,
        )


class UpdateData:
    def __init__(self) -> None:
        self.message_txt = ""
        self.list_reply = None

        # Media
        self.media_mime_type: str = None
        self.media_file_id: str = None
        self.media_hash: str = None
        self.media_voice: bool = False

        # Location
        self.loc_address: str = None
        self.loc_name: str = None
        self.loc_latitude: str = None
        self.loc_longitude: str = None


class UpdateHandler:
    def __init__(self, context: bool = True, *args, **kwargs) -> None:
        self.name: str = None
        self.regex: str = None
        self.func: Callable
        self.action: Callable
        self.context = context
        self.list = None
        self.button = None
        self.persistent = False

    def extract_data(self, msg: Dict[str, dict]) -> UpdateData:
        data = UpdateData()
        data.message_txt = ""
        return data

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
            key: val
            for key, val in kwargs.items()
            if key in inspect.getfullargspec(self.action).args
        }
        return self.action(*args, **new_kwargs)


class MessageHandler(UpdateHandler):
    def __init__(
        self,
        regex: str = None,
        func: Callable = None,
        action: Callable = None,
        context: bool = True,
        persistent: bool = False,
    ) -> None:
        super().__init__(context)
        self.name = "text"
        self.regex = regex
        self.func = func
        self.action = action
        self.persistent = persistent

    def extract_data(self, msg) -> UpdateData:
        data = UpdateData()
        data.message_txt = msg.get("text", {}).get("body", "")
        return data


class InteractiveQueryHandler(UpdateHandler):
    """For button_reply and list_reply"""

    def __init__(
        self,
        regex: str = None,
        func: Callable = None,
        handle_button: bool = True,
        handle_list: bool = True,
        action: Callable = None,
        context: bool = True,
        persistent: bool = False,
    ) -> None:
        super().__init__(context)
        self.name = "interactive"
        self.regex = regex
        self.func = func
        self.action = action
        self.list = handle_list
        self.button = handle_button
        self.persistent = persistent

    def extract_data(self, msg) -> UpdateData:
        message_txt = ""
        if msg["interactive"]["type"] == "button_reply" and self.button:
            message_txt = msg.get("interactive", {}).get("button_reply", {}).get("id")
        elif msg["interactive"]["type"] == "list_reply" and self.list:
            message_txt = msg.get("interactive", {}).get("list_reply", {}).get("id")
        data = UpdateData()
        data.message_txt = message_txt
        return data


class MediaHandler(UpdateHandler):
    def __init__(
        self,
        regex: str = None,
        func: Callable = None,
        action: Callable = None,
        context: bool = True,
        persistent: bool = False,
    ) -> None:
        super().__init__(context)
        self.regex = regex
        self.func = func
        self.action = action
        self.persistent = persistent


class ImageHandler(MediaHandler):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.name = "image"

    def extract_data(self, msg) -> UpdateData:
        data = UpdateData()
        img_data = msg.get("image", {})
        data.message_txt = img_data.get("caption", "")
        data.media_mime_type = img_data.get("mime_type", "")
        data.media_file_id = img_data.get("id", "")
        data.media_hash = img_data.get("sha256", "")
        return data


class AudioHandler(MediaHandler):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.name = "audio"

    def extract_data(self, msg) -> UpdateData:
        data = UpdateData()
        audio_data = msg.get("audio", {})
        data.media_mime_type = audio_data.get("mime_type", "")
        data.media_file_id = audio_data.get("id", "")
        data.media_hash = audio_data.get("sha256", "")
        data.media_voice = audio_data.get("voice", "")
        return data


class VideoHandler(MediaHandler):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.name = "video"

    def extract_data(self, msg) -> UpdateData:
        data = UpdateData()
        vid_data = msg.get("video", {})
        data.message_txt = vid_data.get("caption", "")
        data.media_mime_type = vid_data.get("mime_type", "")
        data.media_file_id = vid_data.get("id", "")
        data.media_hash = vid_data.get("sha256", "")
        return data


class StickerHandler(MediaHandler):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.name = "sticker"

    def extract_data(self, msg) -> UpdateData:
        data = UpdateData()
        stckr_data = msg.get("sticker", {})
        data.media_mime_type = stckr_data.get("mime_type", "")
        data.media_file_id = stckr_data.get("id", "")
        data.media_hash = stckr_data.get("sha256", "")
        return data


class LocationHandler(UpdateHandler):
    def __init__(
        self,
        regex: str = None,
        func: Callable = None,
        action: Callable = None,
        context: bool = True,
        persistent: bool = False,
    ) -> None:
        super().__init__(context)
        self.name = "location"
        self.regex = regex
        self.func = func
        self.action = action
        self.persistent = persistent

    def extract_data(self, msg) -> UpdateData:
        data = UpdateData()
        loc_data = msg.get("location", {})
        loc_name = loc_data.get("name", "")
        data.loc_address = loc_data.get("address", "")
        data.loc_name = loc_data.get("name", "")
        data.loc_latitude = loc_data.get("latitude", "")
        data.loc_longitude = loc_data.get("longitude", "")
        data.message_txt = (
            loc_name + "\n" + data.loc_address
            if data.loc_address
            else f"long - _{data.loc_longitude}_\nlat - _{data.loc_longitude}_"
        )

        return data


class UnknownHandler(UpdateHandler):
    def __init__(
        self,
        regex: str = None,
        func: Callable = None,
        action: Callable = None,
        context: bool = True,
        persistent: bool = False,
    ) -> None:
        super().__init__(context)
        self.name = "unknown"
        self.regex = regex
        self.func = func
        self.action = action
        self.persistent = persistent


class UnsupportedHandler(UpdateHandler):
    def __init__(
        self,
        regex: str = None,
        func: Callable = None,
        action: Callable = None,
        context: bool = True,
        persistent: bool = False,
    ) -> None:
        super().__init__(context)
        self.name = "unsupported"
        self.regex = regex
        self.func = func
        self.action = action
        self.persistent = persistent
