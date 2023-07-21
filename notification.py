from json import dumps
from sys import argv
from httplib2 import Http

WEBHOOK_URL = "https://chat.googleapis.com/v1/spaces/AAAAGxW-rNo/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=MoQuTUQpepCEbMWN6zWvk0z7cuKkM20Z2HPyNyHpP2I"


def main(mess):
    if mess[1] == "post":
        post_message(mess)
    else:
        start_message(mess)
        
def start_message(mess):
    url = WEBHOOK_URL
    mess[2] = mess[2][8:]
    bot_message = {
    "cards": [
        {
        "sections": [
            {
            "widgets": [
                {
                "keyValue": {
                    "content": mess[2],
                    "contentMultiline": "true",
                    "icon": "DESCRIPTION",
                    "topLabel": "Executed Job"
                }
                },
                {
                "keyValue": {
                    "content": "Start build",
                    "contentMultiline": "true",
                    "icon": "BOOKMARK",
                    "topLabel": "Status"
                }
                },
                {
                "keyValue": {
                    "content": mess[3],
                    "contentMultiline": "true",
                    "icon": "PERSON",
                    "topLabel": "Author"
                }
                },
            ]
            }
        ]
        }
    ],
    "text": "<users/all> : Job " + mess[2]
    }
    message_headers = {'Content-Type': 'application/json; charset=UTF-8'}
    http_obj = Http()
    response = http_obj.request(
        uri=url,
        method='POST',
        headers=message_headers,
        body=dumps(bot_message),
    )
    print(response)
        

def post_message(mess):
    url = WEBHOOK_URL
    mess[2] = mess[2][8:]
    bot_message = {
    "cards": [
        {
        "sections": [
            {
            "widgets": [
                {
                "keyValue": {
                    "content": mess[2],
                    "contentMultiline": "true",
                    "icon": "DESCRIPTION",
                    "topLabel": "Executed Job"
                }
                },
                {
                "keyValue": {
                    "content": mess[3],
                    "contentMultiline": "true",
                    "icon": "BOOKMARK",
                    "topLabel": "Status"
                }
                },
                {
                "keyValue": {
                    "content": mess[4],
                    "contentMultiline": "true",
                    "icon": "PERSON",
                    "topLabel": "Author"
                }
                },
                {
                "keyValue": {
                    "content": mess[7] + "ms",
                    "contentMultiline": "true",
                    "icon": "CLOCK",
                    "topLabel": "Elapsed"
                }
                },
                {
                "keyValue": {
                    "content": mess[5],
                    "contentMultiline": "true",
                    "icon": "TICKET",
                    "topLabel": "Commit ID"
                }
                },
                {
                "keyValue": {
                    "content": mess[6],
                    "contentMultiline": "true",
                    "icon": "BOOKMARK",
                    "topLabel": "Build URL"
                }
                },
            ]
            }
        ]
        }
    ],
    "text": "<users/all> : Job " + mess[2]
    }
    message_headers = {'Content-Type': 'application/json; charset=UTF-8'}
    http_obj = Http()
    response = http_obj.request(
        uri=url,
        method='POST',
        headers=message_headers,
        body=dumps(bot_message),
    )
    print(response)


if __name__ == '__main__':
    main(argv)