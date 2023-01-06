# python-whatsapp-bot

A whatsapp client library for python utilizing the [WhatsApp Business Cloud API](https://developers.facebook.com/docs/whatsapp/cloud-api).

[![Made in Nigeria](https://img.shields.io/badge/made%20in-nigeria-008751.svg?style=flat-square)](https://github.com/acekyd/made-in-nigeria)
[![Downloads](https://pepy.tech/badge/python-whatsapp-bot)](https://pepy.tech/project/python-whatsapp-bot)
[![Downloads](https://pepy.tech/badge/python-whatsapp-bot/month)](https://pepy.tech/project/python-whatsapp-bot)
[![Downloads](https://pepy.tech/badge/python-whatsapp-bot/week)](https://pepy.tech/project/python-whatsapp-bot)

## Features supported

- [python-whatsapp-bot](#python-whatsapp-bot)
  - [Features supported](#features-supported)
  - [Getting started](#getting-started)
  - [Setting up](#setting-up)
  - [Initialization](#initialization)
  - [Sending Messages](#sending-messages)
    - [Example](#example)
  - [Sending Interactive Messages](#sending-interactive-messages)
    - [For buttons](#for-buttons)
    - [For lists](#for-lists)
  - [Sending Template Messages](#sending-template-messages)
  - [Handling Incoming Messages](#handling-incoming-messages)
    - [A short note about **Webhooks**](#a-short-note-about-webhooks)
  - [Issues](#issues)
  - [Contributing](#contributing)
  - [References](#references)
  - [All the credit](#all-the-credit)

## Getting started

To start, install with pip:

```bash
pip3 install --upgrade python-whatsapp-bot

```

## Setting up

To get started using this library, you have to obtain a **TOKEN** and **PHONE NUMBER ID** from [Facebook Developer Portal](https://developers.facebook.com/). You get these after setting up a developer account and setting up an app.

[Here is a tutorial on the platform on how to go about the process](https://developers.facebook.com/docs/whatsapp/cloud-api/get-started)

If you followed the tutorial, you should now have a **TOKEN** and **TEST WHATSAPP NUMBER** and its phone_number_id.activeYou might have even already sent your first message on the platform using the provided curl request.

Now you have all you need to start using this library.
**Note:** The given token is temporary. [This tutorial](https://developers.facebook.com/docs/whatsapp/business-management-api/get-started#1--acquire-an-access-token-using-a-system-user-or-facebook-login) on the platform guides you to create a permanent token. [This guide](https://developers.facebook.com/docs/whatsapp/cloud-api/get-started#phone-number) shows how to register an authentic phone number.

## Initialization

To initialize the app instance, you need to specify the `TOKEN` and `phone_number_id` you obtained from the steps above. Note that phone number id is not phone number.

```python
>>> from python_whatsapp_bot import Whatsapp
>>> wa_bot = Whatsapp(number_id='305xxxxxx', token=TOKEN)
```

Once initialized, you can start using some of the bot's features right away.

## Sending Messages

To send a text message

```python
>>> wa_bot.send_message('mobile eg: 2348145xxxxx3', 'Your message here')
```

### Example

Here is an example

```python
>>> wa_bot.send_message('2348945434343', 'Your message here')
```

## Sending Interactive Messages

For buttons and lists, use the same send_message endpoint but with a reply_markup parameter. e.g

### For buttons

```python
>>> from from python_whatsapp_bot import Inline_keyboard # Import inline_keyboard for interactive buttons
>>> wa_bot.send_message('2348945434343', 'This is a message with two buttons',reply_markup=Inline_keyboard(['First button', 'Second button']))
```

### For lists

```python
>>> from python_whatsapp_bot import Inline_list, List_item # Import inline_list and List_item for interactive list
>>> wa_bot.send_message('2348945434343', 'This is a message with lists',reply_markup=Inline_list("Show list",list_items=[[List_item("one list item")]])
```

## Sending Template Messages

To send a pre-approved template message:

```python
>>> wa_bot.send_template_message("255757xxxxxx","hello_world")
```

## Handling Incoming Messages

### A short note about **Webhooks**

For every message sent to your bot business account, whatsapp sends an object containing the message as a post request to a url which you have to provide beforehand. The url you provide should be able to process simple get and post requests. This url is the webhook url, and the object whatsapp sends to your url is the webhook.

Now, you can write a small server with the Python Flask library to handle the webhook requests, but another problem arises if you're developing on a local server; whatsapp will not be able to send requests to your localhost url, so a quick fix would be to deploy your project to an online server each time you make a change to be able to test it.
Once deployed, you can proceed to register the url of your deployed app using [this tutorial](https://developers.facebook.com/docs/whatsapp/business-management-api/guides/set-up-webhooks) from the platform.

If you're like me however, you wouldn't want to always deploy before you test, you want to run everything on local first. In this case, you might decide to use Ngrok to tunnel a live url to your local server, but another issue arises; Since Ngrok generates a new url each time it is restarted, you'd have to constantly log in to facebook servers to register the newly generated url. I presume you don't want that hassle either. In this situation, a webhook forwarder can be deployed to a virtual server like Heroku, and it doesn't get modified. You register the deployed forwarder's url on Whatsapp servers, it receives all the webhook requests and forwards them to your local machine using ngrok.

To continue with this fowarding process, open this repository <https://github.com/Radi-dev/webhook-forwarder> and follow the readme instructions to deploy it and setup a client for it on your device, then register the url following [this guide](https://github.com/Radi-dev/webhook-forwarder).

## Issues

Please open an issue to draw my attention to mistake or suggestion

## Contributing

This is an opensource project under `MIT License` so anyone is welcome to contribute from typo, to source code to documentation, `JUST FORK IT`.

## References

1. [WhatsApp Cloud API official documentation](https://developers.facebook.com/docs/whatsapp/cloud-api/)

## All the credit

1. All contributors
