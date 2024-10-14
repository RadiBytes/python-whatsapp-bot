import mimetypes
import os
from pathlib import Path
import re
from typing import Union
import json
import requests
from .markup import (
    Reply_markup,
    Inline_button,
    Inline_keyboard,
    Inline_list,
    List_item,
    List_section,
)

TIMEOUT: int = 30
KNOWN_EXTENSIONS = {
    "text/plain": ".txt",
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/gif": ".gif",
    "video/mp4": ".mp4",
    "audio/mp3": ".mp3",
    "audio/mpeg": ".mp3",
    "audio/wav": ".wav",
    "audio/aac": ".aac",
    "audio/ogg": ".opus",
    "audio/webm": ".webm",
    "application/pdf": ".pdf",
    "application/msword": ".doc",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
    "application/vnd.ms-powerpoint": ".ppt",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation": ".pptx",
    "application/vnd.ms-excel": ".xls",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": ".xlsx",
}


def headers(WA_TOKEN):
    return {"Content-Type": "application/json", "Authorization": f"Bearer {WA_TOKEN}"}


def mark_as_read(update, url: str, token: str):
    payload = json.dumps(
        {"messaging_product": "whatsapp", "status": "read", "message_id": update["id"]}
    )
    response = requests.post(url, headers=headers(token), data=payload, timeout=TIMEOUT)
    return response


def message_text(
    url: str,
    token: str,
    phone_num: str,
    text: str,
    msg_id: str = "",
    web_page_preview=True,
    tag_message: bool = True,
):
    message_frame = {
        "messaging_product": "whatsapp",
        "to": str(phone_num),
        "recipient_type": "individual",
        "type": "text",
        "text": {"body": text, "preview_url": web_page_preview},
    }
    if msg_id and tag_message:
        message_frame["context"] = {"message_id": msg_id}
    payload = json.dumps(message_frame)
    response = requests.post(url, headers=headers(token), data=payload, timeout=TIMEOUT)
    return response


def message_interactive(
    url: str,
    token: str,
    phone_num: str,
    text: str,
    reply_markup: Reply_markup,
    msg_id: str = "",
    header: str = None,
    header_type: str = "text",
    footer: str = None,
    web_page_preview=True,
):
    if not isinstance(reply_markup, Reply_markup):
        raise ValueError("Reply markup must be a Reply_markup object")
    message_frame = {
        "messaging_product": "whatsapp",
        "to": str(phone_num),
        "recipient_type": "individual",
        "type": "interactive",
        "interactive": {
            "type": _get_markup_type(reply_markup),
            "body": {"text": text},
            "action": reply_markup.markup,
        },
    }
    if msg_id:
        message_frame["context"] = {"message_id": msg_id}
    if header:
        if header_type == "text":
            message_frame["interactive"]["header"] = {
                "type": "text",  # [text,video,image,document]
                "text": header,
            }
        elif header_type in ["image", "video", "document"]:
            if re.match(r"^((http[s]?://)|(www.))", header):
                header_type_object = {"link": header}
            else:
                header_type_object = {"id": header}
            message_frame["interactive"]["header"] = {
                "type": header_type,  # [text,video,image,document]
                header_type: header_type_object,
            }

    if footer:
        message_frame["interactive"]["footer"] = {"text": footer}
    payload = json.dumps(message_frame)
    response = requests.post(url, headers=headers(token), data=payload, timeout=TIMEOUT)
    return response


def message_template(
    url: str,
    token: str,
    phone_num: str,
    template_name: str,
    components: list = None,
    language_code: str = "en_US",
):
    payload = json.dumps(
        {
            "messaging_product": "whatsapp",
            "to": str(phone_num),
            "recipient_type": "individual",
            "type": "template",
            "template": {
                "name": template_name,
                "language": {"code": language_code},
                "components": list(components) if components is not None else [],
            },
        }
    )
    response = requests.post(url, headers=headers(token), data=payload, timeout=TIMEOUT)
    return response


def _get_markup_type(markup):
    if isinstance(markup, Inline_keyboard):
        return "button"
    elif isinstance(markup, Inline_list):
        return "list"


def upload_media(url: str, token: str):
    payload = json.dumps(
        {
            "messaging_product": "whatsapp",
        }
    )
    response = requests.post(url, headers=headers(token), data=payload, timeout=TIMEOUT)
    return response


def get_media_url(base_url: str, media_id: str, token: str):
    url = f"{base_url}/{media_id}"
    print(url)
    response = requests.get(url, headers=headers(token), timeout=TIMEOUT)
    return response


def download_media(
    base_url: str, media_id: str, token: str, relative_file_path: str = "/media"
):
    # Generate the absolute file path from the relative path
    file_path = Path("tmp/" + relative_file_path).resolve() / media_id

    # Ensure the file has the correct extension
    media_data = get_media_url(base_url, media_id, token).json()
    media_url = media_data["url"]
    mime_type = media_data["mime_type"]
    extension = (
        KNOWN_EXTENSIONS.get(mime_type)
        or mimetypes.guess_extension(mime_type, strict=True)
        or ".bin"
    )

    file_path = file_path.with_suffix(extension)

    # Create the directory if it does not exist
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # Download the media file
    with requests.get(
        media_url, headers=headers(token), stream=True, timeout=TIMEOUT
    ) as response, open(file_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)

    return response


def message_media(
    url: str,
    token: str,
    phone_num: str,
    image_path: str,
    caption: str = None,
    media_provider_token: str = None,
):
    payload = json.dumps(
        {
            "messaging_product": "whatsapp",
            "to": str(phone_num),
            "recipient_type": "individual",
            "type": "image",
            "image": {
                # "id" : "MEDIA-OBJECT-ID"
                "link": image_path,
                "caption": caption,
            },
        }
    )
    response = requests.post(url, headers=headers(token), data=payload, timeout=TIMEOUT)
    return response


def message_location(
    url: str, token: str, phone_num: str, text: str, web_page_preview=True
):
    payload = json.dumps(
        {
            "messaging_product": "whatsapp",
            "to": str(phone_num),
            "recipient_type": "individual",
            "type": "text",
            "text": {"body": text, "preview_url": web_page_preview},
        }
    )
    response = requests.post(url, headers=headers(token), data=payload, timeout=TIMEOUT)
    return response
