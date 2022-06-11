general_template = {"object": "whatsapp_business_account",
                    "entry": [{
                        "id": "WHATSAPP-BUSINESS-ACCOUNT-ID",
                        "changes": [{
                            "value": {
                                "messaging_product": "whatsapp",
                                "metadata": {
                                    "display_phone_number": "PHONE-NUMBER",
                                    "phone_number_id": "PHONE-NUMBER-ID"
                                },
                                # Additional arrays and objects
                                "contacts": [{}],
                                "errors": [{}],
                                "messages": [{}],
                                "statuses": [{}]
                            },
                            "field": "messages"
                        }]
                    }]
                    }

sample_text_rcvd = {'from': '2348138686782',
                    'id': 'wamid.HBgNMjM0ODEzODY4Njc4MhUCABIYIEUyQjMzRDdFOUY1RTk3QzVFOTYzNkU0QTNCM0JERUY1AA==',
                    'timestamp': '1654924099',
                    'text': {
                        'body': 'https://radidev.com/'
                    },
                    'type': 'text'
                    }

sample_sticker_received = {'from': '2348138686782',
                           'id': 'wamid.HBgNMjM0ODEzODY4Njc4MhUCABIYIEQ0Mzg4Q0YxOTUyMzMxRTE3RUQ1NkUwQUVEM0NFRUQzAA==',
                           'timestamp': '1654958736',
                           'type': 'sticker',
                           'sticker': {
                               'mime_type': 'image/webp',
                               'sha256': 'FemlwCo9v3a+hxpZg3Ils7Amx1sXHlvFVNx/Ta5kadQ=',
                               'id': '575477140657709'}}

sample_contact_rcvd = {'from': '2348138686782',
                       'id': 'wamid.HBgNMjM0ODEzODY4Njc4MhUCABIYIDA2RDgwQTIwRTg1M0FDQjk3RjgyRTJCQUE0NkYzNDNEAA==',
                       'timestamp': '1654958900',
                       'type': 'contacts',
                       'contacts': [
                           {
                               'name': {
                                   'first_name': 'Faithfulness',
                                   'last_name': 'Obasi-kalu',
                                   'formatted_name': 'Faithfulness Obasi-kalu'
                               },
                               'phones': [{
                                   'phone': '+234 907 106 4387',
                                   'wa_id': '2349071064387',
                                   'type': 'Mobile'}]}]}
sample_location_rcvd = {'from': '2348138686782',
                        'id': 'wamid.HBgNMjM0ODEzODY4Njc4MhUCABIYIEEyRjFEMDExOThDQ0MxOTI2RDE1NTg2NzQ3MTg3MDE5AA==',
                        'timestamp': '1654959120',
                        'location': {
                            'latitude': 6.2355939,
                            'longitude': 7.0900079
                        },
                        'type': 'location'}
sample_interactive_btn_rcvd = {'context': {
    'from': '2349040024090',
    'id': 'wamid.HBgNMjM0ODEzODY4Njc4MhUCABEYEjBEQjIzMzg4RjUyRUI2NjY5RAA='
},
    'from': '2348138686782',
    'id': 'wamid.HBgNMjM0ODEzODY4Njc4MhUCABIYIDg3RjExRkQ4OEYyMThCQ0NCRTIxQjUyODlEREUzOUQ2AA==',
    'timestamp': '1654960074',
    'type': 'interactive',
    'interactive': {
        'type': 'button_reply',
        'button_reply': {
            'id': 'Button 1',
            'title': 'Button 1'
        }}}

sample_interactive_list_rcvd = {'context': {
    'from': '2349040024090',
    'id': 'wamid.HBgNMjM0ODEzODY4Njc4MhUCABEYEkUzMDUxREJEMENBNzIzRjQ5OAA='
},
    'from': '2348138686782',
    'id': 'wamid.HBgNMjM0ODEzODY4Njc4MhUCABIYIEY1QTEwQkJBMzMwNEQ1MDgyRjI3RTFBMjlDNUY1MDVFAA==',
    'timestamp': '1654960638',
    'type': 'interactive',
    'interactive': {
    'type': 'list_reply',
    'list_reply': {
        'id': 'two list',
        'title': 'two list'
    }}}

sample_image_rcvd = {'from': '2348138686782',
                     'id': 'wamid.HBgNMjM0ODEzODY4Njc4MhUCABIYIDEwODI0QzY5NDcyQ0Q2QjRDRUQzMzVCOTE1ODY1N0JDAA==',
                     'timestamp': '1654960306',
                     'type': 'image',
                     'image': {
                         'mime_type': 'image/jpeg',
                         'sha256': 'TIvl2pJlkcSWd0/qxxHLzZ7FwnrFmMURoMIh0VLlcVI=',
                         'id': '1117630378790438'}}
