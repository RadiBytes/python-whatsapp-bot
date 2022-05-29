import requests
import json

url = "https://graph.facebook.com/v13.0/101679669228626/messages"

payload = json.dumps({
    "messaging_product": "whatsapp",
    "to": "2348138686782",
    "recipient_type": "individual",
    "type": "interactive",
    "interactive": {
        "type": "button",
        "header": {"type": "text", "text": "Okay ohh"},
        "body": {
            "text": "BUTTON_TEXT"
        },
        "action": {
            "buttons": [
                {
                    "type": "reply",
                    "reply": {
                        "id": "UNIQUE_BUTTON_ID_1",
                        "title": "UNIQUE_BUTTON_ID_1"
                    }
                },
                {
                    "type": "reply",
                    "reply": {
                        "id": "butt2",
                        "title": "butt2"
                    }
                }
            ]
        }
    }
})
payl = json.dumps({
    "messaging_product": "whatsapp",
    "to": "2348138686782",
    "recipient_type": "individual",
    "type": "template",
    "template": {
        "name": "hi",
        "language": {
            "code": "LANGUAGE_AND_LOCALE_CODE"
        },
        "components": [
            {
                "type": "header",
                "parameters": [
                    {
                        "type": "image",
                        "image": {
                            "link": "https://source.unsplash.com/gySMaocSdqs"
                        }
                    }
                ]
            },
            {
                "type": "body",
                "parameters": [
                    {
                        "type": "text",
                        "text": "TEXT_STRING"
                    },
                    {
                        "type": "currency",
                        "currency": {
                            "fallback_value": "VALUE",
                            "code": "USD",
                            "amount_1000": 2344
                        }
                    },
                    {
                        "type": "date_time",
                        "date_time": {
                            "fallback_value": "MONTH DAY, YEAR"
                        }
                    }
                ]
            },
            {
                "type": "button",
                "sub_type": "quick_reply",
                "index": "0",
                "parameters": [
                    {
                        "type": "payload",
                        "payload": "PAYLOAD"
                    }
                ]
            },
            {
                "type": "button",
                "sub_type": "quick_reply",
                "index": "1",
                "parameters": [
                    {
                        "type": "payload",
                        "payload": "PAYLOAD"
                    }
                ]
            }
        ]
    }})
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer EAAak5hlwhZBgBAJ67X1ICFQtR9cfAXjK61E8ZCzb8mMwozmO245VhIIbl2WgLteFKV3cDMnUEDxchyXjBhN4EBnbkSlxdLHHZCnaHpKcgyIWbnvL8jkPYAPf4MKvRBPqMD7Tyf8D3XZBB2dqcWO2brioAbfsGR6aB05maaa3ksyIEScl4UZCB'
}

#response = requests.request("POST", url, headers=headers, data=payload)
response = requests.post(url, headers=headers, data=payload)

print(response.text)
