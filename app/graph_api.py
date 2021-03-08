"""app/graph_api.py
"""
import codecs
import json

import requests

from app import graph_url
from app.get_access_token import get_access_token


def graph_api(service):
    """graph_api
    """
    url = '{graph_url}{service}'.format(**{
        'graph_url': graph_url,
        'service': service
    })

    headers = {
        "Authorization": get_access_token()
    }

    res = requests.get(url=url, headers=headers)

    print(res.status_code)
    print(codecs.decode(json.dumps(json.loads(res.text), indent=4), 'unicode-escape'))


if __name__ == '__main__':
    graph_api(service='/sites/{hostname}:/{server-relative-path}')
