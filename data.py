general_template = {
    "object": "whatsapp_business_account",
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
                "contacts": [{...}]
                "errors": [{...}]
                "messages": [{...}]
                "statuses": [{...}]
            },
            "field": "messages"
        }]
    }]
}

txt_msg_sample = {
    "object": "whatsapp_business_account",
    "entry": [{
        "id": "WHATSAPP_BUSINESS_ACCOUNT_ID",
        "changes": [{
            "value": {
              "messaging_product": "whatsapp",
              "metadata": {
                  "display_phone_number": PHONE_NUMBER,
                  "phone_number_id": PHONE_NUMBER_ID
              },
                "contacts": [{
                    "profile": {
                        "name": "NAME"
                    },
                    "wa_id": PHONE_NUMBER
                }],
                "messages": [{
                    "from": PHONE_NUMBER,
                    "id": "wamid.ID",
                    "timestamp": TIMESTAMP,
                    "text": {
                        "body": "MESSAGE_BODY"
                    },
                    "type": "text"
                }]
            },
            "field": "messages"
        }]
    }]
}

media_msg_sample = {
    "object": "whatsapp_business_account",
    "entry": [{
        "id": "WHATSAPP_BUSINESS_ACCOUNT_ID",
        "changes": [{
            "value": {
              "messaging_product": "whatsapp",
              "metadata": {
                  "display_phone_number": PHONE_NUMBER,
                  "phone_number_id": PHONE_NUMBER_ID
              },
                "contacts": [{
                    "profile": {
                        "name": "NAME"
                    },
                    "wa_id": "WHATSAPP_ID"
                }],
                "messages": [{
                    "from": PHONE_NUMBER,
                    "id": "wamid.ID",
                    "timestamp": TIMESTAMP,
                    "type": "image",
                    "image": {
                        "caption": "CAPTION",
                        "mime_type": "image/jpeg",
                        "sha256": "IMAGE_HASH",
                        "id": "ID"
                    }
                }]
            },
            "field": "messages"
        }]
    }]
}

sticker_msg_sample = {
    "object": "whatsapp_business_account",
    "entry": [
        {
            "id": "ID",
            "changes": [
              {
                  "value": {
                      "messaging_product": "whatsapp",
                      "metadata": {
                          "display_phone_number": "PHONE_NUMBER",
                          "phone_number_id": "PHONE_NUMBER_ID"
                      },
                      "contacts": [
                          {
                              "profile": {
                                  "name": "NAME"
                              },
                              "wa_id": "ID"
                          }
                      ],
                      "messages": [
                          {
                              "from": "SENDER_PHONE_NUMBER",
                              "id": "wamid.ID",
                              "timestamp": "TIMESTAMP",
                              "type": "sticker",
                              "sticker": {
                                  "mime_type": "image/webp",
                                  "sha256": "HASH",
                                  "id": "ID"
                              }
                          }
                      ]
                  },
                  "field": "messages"
              }
            ]
        }
    ]
}

unknown_msg_sample = {
    "object": "whatsapp_business_account",
    "entry": [{
        "id": "WHATSAPP_BUSINESS_ACCOUNT_ID",
        "changes": [{
            "value": {
              "messaging_product": "whatsapp",
              "metadata": {
                  "display_phone_number": "PHONE_NUMBER",
                  "phone_number_id": "PHONE_NUMBER_ID"
              },
                "contacts": [{
                    "profile": {
                        "name": "NAME"
                    },
                    "wa_id": "WHATSAPP_ID"
                }],
                "messages": [{
                    "from": "PHONE_NUMBER",
                    "id": "wamid.ID",
                    "timestamp": "TIMESTAMP",
                    "errors": [
                        {
                          "code": 131051,
                          "details": "Message type is not currently supported",
                          "title": "Unsupported message type"
                        }],
                    "type": "unknown"
                }]
            }
            "field": "messages"
        }],
    }]
}

location_msg_sample = {
    "object": "whatsapp_business_account",
    "entry": [{
        "id": "WHATSAPP_BUSINESS_ACCOUNT_ID",
        "changes": [{
            "value": {
              "messaging_product": "whatsapp",
              "metadata": {
                  "display_phone_number": "PHONE_NUMBER",
                  "phone_number_id": "PHONE_NUMBER_ID"
              },
                "contacts": [{
                    "profile": {
                        "name": "NAME"
                    },
                    "wa_id": "WHATSAPP_ID"
                }],
                "messages": [{
                    "from": "PHONE_NUMBER",
                    "id": "wamid.ID",
                    "timestamp": "TIMESTAMP",
                    "location": {
                        "latitude": LOCATION_LATITUDE,
                        "longitude": LOCATION_LONGITUDE,
                        "name": LOCATION_NAME,
                        "address": LOCATION_ADDRESS,
                    }
                }]
            },
            "field": "messages"
        }]
    }]
}
contact_msg_sample = {
    "object": "whatsapp_business_account",
    "entry": [{
        "id": "WHATSAPP_BUSINESS_ACCOUNT_ID",
        "changes": [{
            "value": {
                "messaging_product": "whatsapp",
                "metadata": {
                    "display_phone_number": "PHONE_NUMBER",
                    "phone_number_id": "PHONE_NUMBER_ID"
                },
                "contacts": [{
                    "profile": {
                        "name": "NAME"
                    },
                    "wa_id": "WHATSAPP_ID"
                }],
                "messages": [{
                    "from": "PHONE_NUMBER",
                    "id": "wamid.ID",
                    "timestamp": "TIMESTAMP",
                    "contacts": [{
                        "addresses": [{
                            "city": "CONTACT_CITY",
                            "country": "CONTACT_COUNTRY",
                            "country_code": "CONTACT_COUNTRY_CODE",
                            "state": "CONTACT_STATE",
                            "street": "CONTACT_STREET",
                            "type": "HOME or WORK",
                            "zip": "CONTACT_ZIP"
                        }],
                        "birthday": "CONTACT_BIRTHDAY",
                        "emails": [{
                            "email": "CONTACT_EMAIL",
                            "type": "WORK or HOME"
                        }],
                        "name": {
                            "formatted_name": "CONTACT_FORMATTED_NAME",
                            "first_name": "CONTACT_FIRST_NAME",
                            "last_name": "CONTACT_LAST_NAME",
                            "middle_name": "CONTACT_MIDDLE_NAME",
                            "suffix": "CONTACT_SUFFIX",
                            "prefix": "CONTACT_PREFIX"
                        },
                        "org": {
                            "company": "CONTACT_ORG_COMPANY",
                            "department": "CONTACT_ORG_DEPARTMENT",
                            "title": "CONTACT_ORG_TITLE"
                        },
                        "phones": [{
                            "phone": "CONTACT_PHONE",
                            "wa_id": "CONTACT_WA_ID",
                            "type": "HOME or WORK>"
                        }],
                        "urls": [{
                            "url": "CONTACT_URL",
                            "type": "HOME or WORK"
                        }]
                    }]
                }]
            },
            "field": "messages"
        }]
    }]
}

button_select = {
    "object": "whatsapp_business_account",
    "entry": [
        {
            "id": "WHATSAPP_BUSINESS_ACCOUNT_ID",
            "changes": [
              {
                  "value": {
                      "messaging_product": "whatsapp",
                      "metadata": {
                          "display_phone_number": "PHONE_NUMBER",
                          "phone_number_id": PHONE_NUMBER_ID,
                      },
                      "contacts": [
                          {
                              "profile": {
                                  "name": "NAME"
                              },
                              "wa_id": "PHONE_NUMBER_ID"
                          }
                      ],
                      "messages": [
                          {
                              "from": PHONE_NUMBER_ID,
                              "id": "wamid.ID",
                              "timestamp": TIMESTAMP,
                              "interactive": {
                                  "button_reply": {
                                      "id": "unique-button-identifier-here",
                                      "title": "button-text",
                                  },
                                  "type": "button_reply"
                              },
                              "type": "interactive"
                          }
                      ]
                  },
                  "field": "messages"
              }
            ]
        }
    ]
}
