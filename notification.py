from json import dumps
from sys import argv
from httplib2 import Http
import env_db_vars
import psycopg2


web_hook_url = env_db_vars.GOOGLE_CHAT_WEBHOOK_URL

def main(mess):
    if mess[1] == "success":
        post_message(mess)
    elif mess[1] == "start":
        start_message(mess)
    elif mess[1] == "approval":
        approval_message(mess)
    elif mess[1] == "failure":
        failure_message(mess)
    elif mess[1] == "aborted":
        aborted_message(mess)
        
def approval_message(mess):
    url = web_hook_url
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
                    "topLabel": "Executing Job at Branch"
                }
                },
                {
                "keyValue": {
                    "content": "Waiting for Approval: \nMissing module upgrade: " + mess[4],
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
                {
                "keyValue": {
                    "content": mess[6],
                    "contentMultiline": "true",
                    "icon": "BOOKMARK",
                    "topLabel": "Build URL"
                }
                },
                {
                "keyValue": {
                    "content": mess[-1],
                    "contentMultiline": "true",
                    "icon": "TICKET",
                    "topLabel": "Commit ID"
                }
                },
            ]
            }
        ]
        }
    ],
    "text": " <users/{}> : Job {}".format(mess[5], mess[2])
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
        
def start_message(mess):
    url = web_hook_url
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
                    "topLabel": "Executed Job at Branch"
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
                {
                "keyValue": {
                    "content": mess[4],
                    "contentMultiline": "true",
                    "icon": "TICKET",
                    "topLabel": "Commit ID"
                }
                },
            ]
            }
        ]
        }
    ],
    "text": " <users/{}> : Job {}".format(mess[5], mess[2])
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
    url = web_hook_url
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
                    "topLabel": "Executed Job at Branch"
                }
                },
                {
                "keyValue": {
                    "content": mess[3] + '\nModule upgraded: ' + mess[9],
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
                    "content": mess[8] + "ms",
                    "contentMultiline": "true",
                    "icon": "CLOCK",
                    "topLabel": "Elapsed"
                }
                },
                {
                "keyValue": {
                    "content": mess[6],
                    "contentMultiline": "true",
                    "icon": "TICKET",
                    "topLabel": "Commit ID"
                }
                },
                {
                "keyValue": {
                    "content": mess[7],
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
    "text": " <users/{}> : Job {}".format(mess[5], mess[2])
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

def failure_message(mess):
    url = web_hook_url
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
                    "topLabel": "Executed Job at Branch"
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
                    "content": mess[6],
                    "contentMultiline": "true",
                    "icon": "TICKET",
                    "topLabel": "Commit ID"
                }
                },
                {
                "keyValue": {
                    "content": mess[8],
                    "contentMultiline": "true",
                    "icon": "CLOCK",
                    "topLabel": "Failure Stage:"
                }
                },
                {
                "keyValue": {
                    "content": mess[7],
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
    "text": " <users/{}> : Job {}".format(mess[5], mess[2])
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

def aborted_message(mess):
    url = web_hook_url
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
                    "topLabel": "Executed Job at Branch"
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
                    "content": mess[6],
                    "contentMultiline": "true",
                    "icon": "TICKET",
                    "topLabel": "Commit ID"
                }
                },
                {
                "keyValue": {
                    "content": mess[7],
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
    "text": " <users/{}> : Job {}".format(mess[5], mess[2])
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