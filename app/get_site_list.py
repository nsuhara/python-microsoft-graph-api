"""app/get_site_list.py
[リスト内のアイテムを列挙する](https://docs.microsoft.com/ja-jp/graph/api/listitem-list?view=graph-rest-1.0&tabs=http)
"""
from app.graph_api import graph_api

"""サイトID取得
curl -H 'Authorization: Bearer {access_token}' \
-X GET 'https://graph.microsoft.com/v1.0/sites/{hostname}:/{server-relative-path}'
"""
graph_api(service='/sites/{hostname}:/{server-relative-path}')

"""サイトリスト取得
curl -H 'Authorization: Bearer {access_token}' \
-X GET 'https://graph.microsoft.com/v1.0/sites/{siteId}/lists'
"""
graph_api(service='/sites/{siteId}/lists')

"""リストアイテム取得
curl -H 'Authorization: Bearer {access_token}' \
-X GET 'https://graph.microsoft.com/v1.0/sites/{siteId}/lists/{list-id}/items'
"""
graph_api(service='/sites/{siteId}/lists/{list-id}/items')

"""リストアイテム取得(select)
curl -H 'Authorization: Bearer {access_token}' \
-X GET 'https://graph.microsoft.com/v1.0/sites/{siteId}/lists/{list-id}/items?expand=fields(select=id,Title,Body)'
"""
graph_api(service='/sites/{siteId}/lists/{list-id}/items?expand=fields(select=id,Title,Body)')
