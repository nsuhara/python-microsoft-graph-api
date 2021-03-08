"""app/get_drive_data.py
[DriveItemのコンテンツをダウンロードする](https://docs.microsoft.com/ja-jp/graph/api/driveitem-get-content?view=graph-rest-1.0&tabs=http)
"""
from app.graph_api import graph_api

"""サイト検索
curl -H 'Authorization: Bearer {access_token}' \
-X GET 'https://graph.microsoft.com/v1.0/sites?search={string}'
"""
graph_api(service='/sites?search={string}')

"""サイトのドライブ一覧取得
curl -H 'Authorization: Bearer {access_token}' \
-X GET 'https://graph.microsoft.com/v1.0/sites/{siteId}/drives'
"""
graph_api(service='/sites/{siteId}/drives')

"""ドライブのルート一覧取得
curl -H 'Authorization: Bearer {access_token}' \
-X GET 'https://graph.microsoft.com/v1.0/drives/{drive-id}/root/children'
"""
graph_api(service='/drives/{drive-id}/root/children')

"""ルートの子一覧取得
curl -H 'Authorization: Bearer {access_token}' \
-X GET 'https://graph.microsoft.com/v1.0/drives/{drive-id}/items/{item-id}/children'
"""
graph_api(service='/drives/{drive-id}/items/{item-id}/children')

"""コンテンツ取得
curl -H 'Authorization: Bearer {access_token}' \
-X GET 'https://graph.microsoft.com/v1.0/drives/{drive-id}/items/{item-id}/content'
"""
graph_api(service='/drives/{drive-id}/items/{item-id}/content')
