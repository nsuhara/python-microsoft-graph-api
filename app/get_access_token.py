"""app/get_access_token.py
curl -d 'client_id={client_id}' \
-d 'scope=https://graph.microsoft.com/.default' \
-d 'client_secret={client_secret}' \
-d 'grant_type=client_credentials' \
-H 'Content-Type: application/x-www-form-urlencoded' \
-X POST 'https://login.microsoftonline.com/{tennant_id}/oauth2/v2.0/token'
"""
import json

import requests

from app import client_id, client_secret, grant_type, scope, tennant_id


def get_access_token():
    """get_access_token
    """
    url = 'https://login.microsoftonline.com/{tennant_id}/oauth2/v2.0/token'.format(**{
        'tennant_id': tennant_id
    })

    data = {
        'client_id': client_id,
        'scope': scope,
        'client_secret': client_secret,
        'grant_type': grant_type
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    res = requests.post(url=url, data=data, headers=headers)

    return json.loads(res.text).get('access_token')


if __name__ == '__main__':
    print(get_access_token())
