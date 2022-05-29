from typing import Union
import json
import requests
from .markup import Reply_markup, Inline_button, Inline_keyboard, Inline_list, List_item, List_section


def headers(WA_TOKEN):
    return {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {WA_TOKEN}"}


def message_text(url: str, token: str, phone_num: int, text: str, web_page_preview=True):
    payload = json.dumps({
        "messaging_product": "whatsapp",
        "to": str(phone_num),
        "recipient_type": "individual",
        "type": "text",
        "text": {
            "body": text,
            "preview_url": web_page_preview}})
    response = requests.post(url, headers=headers(token), data=payload)
    print(response.text)
    return response


def message_interactive(url: str, token: str, phone_num: int, text: str, reply_markup: Reply_markup, header: str = None, footer: str = None, web_page_preview=True):
    if not isinstance(reply_markup, Reply_markup):
        raise ValueError("Reply markup must be a Reply_markup object")
    message_frame = {
        "messaging_product": "whatsapp",
        "to": str(phone_num),
        "recipient_type": "individual",
        "type": "interactive",
        "interactive": {
            "type": get_markup_type(reply_markup),
            "body": {
                "text": text
            },
            "action": reply_markup.markup}}
    if header:
        message_frame["interactive"]["header"] = {
            "type": "text",
            "text": header
        }
    if footer:
        message_frame["interactive"]["footer"] = {
            "text": footer
        }
    print(message_frame)
    payload = json.dumps(message_frame)
    response = requests.post(url, headers=headers(token), data=payload)
    print(response.text)
    return response


def get_markup_type(markup):
    if isinstance(markup, Inline_keyboard):
        return "button"
    elif isinstance(markup, Inline_list):
        return "list"


def message_location(url: str, token: str, phone_num: int, text: str, web_page_preview=True):
    payload = json.dumps({
        "messaging_product": "whatsapp",
        "to": str(phone_num),
        "recipient_type": "individual",
        "type": "text",
        "text": {
            "body": text,
            "preview_url": web_page_preview}})
    response = requests.post(url, headers=headers(token), data=payload)
    print(response.text)
    return response
