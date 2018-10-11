import requests
import json
from slackclient import SlackClient

webhook_url = "https://hooks.slack.com/services/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"
slack_token = "xoxp-5133211795-5133211811-265540341936-7bb35486d453e24457f174a6d64922c5"
sc = SlackClient(slack_token)


post_json = {
    "text": "text",
    "attachments": [
        {
            "fields": [{
                "title": "user",
                "value": "kotatsu_mi"
            }],
            "image_url": "https://pbs.twimg.com/profile_images/1034675040527118336/ssvaL0-F_bigger.jpg"
        },
        {
            "fields": [{
                "title": "test2",
                "value": "test3"
            }],
            "image_url": "https://pbs.twimg.com/media/Dm0DUNwUwAIqrcL.jpg"
        }

    ]
}

response = requests.post(webhook_url, data=json.dumps(post_json))

post2_json = {
    "text": "/clip today",
}

# response = requests.post(webhook_url, data=json.dumps(post2_json))

# sc.api_call(
#     "chat.postMessage",
#     channel="CCRCBKEEP",
#     text="test text from legacy api"
# )
# 
sc.api_call(
    "chat.command",
    channel="CCRCBKEEP",
    command="/clip",
    text='last hogehoge'
)