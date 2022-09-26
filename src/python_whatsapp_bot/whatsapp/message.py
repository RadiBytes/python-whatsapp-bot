import re
from typing import Union
import json
import requests
from .markup import Reply_markup, Inline_button, Inline_keyboard, Inline_list, List_item, List_section


def headers(WA_TOKEN):
    return {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {WA_TOKEN}"}


def mark_as_read(update, url: str, token: str):
    payload = json.dumps({"messaging_product": "whatsapp",
                          "status": "read",
                          "message_id": update["id"]
                          })
    response = requests.post(url, headers=headers(token), data=payload)
    # print(response.text)
    return response


def message_text(url: str, token: str, phone_num: str, text: str, web_page_preview=True):
    payload = json.dumps({
        "messaging_product": "whatsapp",
        "to": str(phone_num),
        "recipient_type": "individual",
        "type": "text",
        "text": {
            "body": text,
            "preview_url": web_page_preview}})
    response = requests.post(url, headers=headers(token), data=payload)
    # print(response.text)
    return response


def message_interactive(url: str, token: str, phone_num: str, text: str, reply_markup: Reply_markup, header: str = None, header_type: str = "text", footer: str = None, web_page_preview=True):
    if not isinstance(reply_markup, Reply_markup):
        raise ValueError("Reply markup must be a Reply_markup object")
    message_frame = {
        "messaging_product": "whatsapp",
        "to": str(phone_num),
        "recipient_type": "individual",
        "type": "interactive",
        "interactive": {
            "type": _get_markup_type(reply_markup),
            "body": {
                "text": text
            },
            "action": reply_markup.markup}}
    if header:
        if header_type == 'text':
            message_frame["interactive"]["header"] = {
                "type": 'text',  # [text,video,image,document]
                "text": header
            }
        elif header_type in ['image', 'video', 'document']:
            if re.match(r"^((http[s]?://)|(www.))", header):
                header_type_object = {'link': header}
            else:
                header_type_object = {'id': header}
            message_frame["interactive"]["header"] = {
                "type": header_type,  # [text,video,image,document]
                header_type: header_type_object
            }

    if footer:
        message_frame["interactive"]["footer"] = {
            "text": footer
        }
    payload = json.dumps(message_frame)
    response = requests.post(url, headers=headers(token), data=payload)
    return response


def message_template(url: str, token: str, phone_num: str, template_name: str):
    payload = json.dumps({
        "messaging_product": "whatsapp",
        "to": str(phone_num),
        "recipient_type": "individual",
        "type": "template",
                "template": {
                    "name": template_name,
                    "language": {
                        "code": "en_US"
                    }}})
    response = requests.post(url, headers=headers(token), data=payload)
    # print(response.text)
    return response


def _get_markup_type(markup):
    if isinstance(markup, Inline_keyboard):
        return "button"
    elif isinstance(markup, Inline_list):
        return "list"


def upload_media(url: str, token: str,):
    payload = json.dumps({
        "messaging_product": "whatsapp",
    })
    response = requests.post(url, headers=headers(token), data=payload)
    # print(response.text)
    return response


def message_media(url: str, token: str, phone_num: str, image_path: str, caption: str = None, media_provider_token: str = None):
    payload = json.dumps({
        "messaging_product": "whatsapp",
        "to": str(phone_num),
        "recipient_type": "individual",
        "type": "image",
        "image": {
            # "id" : "MEDIA-OBJECT-ID"
            "link": image_path,
            "caption": caption
        }})
    response = requests.post(url, headers=headers(token), data=payload)
    # print(response.text)
    return response


def message_location(url: str, token: str, phone_num: str, text: str, web_page_preview=True):
    payload = json.dumps({
        "messaging_product": "whatsapp",
        "to": str(phone_num),
        "recipient_type": "individual",
        "type": "text",
        "text": {
            "body": text,
            "preview_url": web_page_preview}})
    response = requests.post(url, headers=headers(token), data=payload)
    # print(response.text)
    return response
