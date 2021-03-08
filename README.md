# Microsoft Graph API でクラウドサービスのデータを取得する

## はじめに

`Mac環境の記事ですが、Windows環境も同じ手順になります。環境依存の部分は読み替えてお試しください。`

### 目的

Microsoft Graph (REST API) を使用して各サービスのデータを取得します。この記事では `ユーザーなしでアクセスを取得` と `SharePoint` と `OneDrive` の方法をご紹介します。

- Microsoft 365 サービス: Delve, Excel, Microsoft Bookings, Microsoft Teams, OneDrive, OneNote, Outlook/Exchange, Planner, SharePoint, Workplace Analytics
- Enterprise Mobility + セキュリティサービス: Advanced Threat Analytics, Advanced Threat Protection, Azure Active Directory, Identity Manager, Intune
- Windows 10 サービス: アクティビティ, デバイス, 通知, ユニバーサル印刷 (プレビュー)
- Dynamics 365 Business Central

この記事を最後まで読むと、次のことができるようになります。

| No.  | 概要                       | キーワード                   |
| :--- | :------------------------- | :--------------------------- |
| 1    | 認証トークン の種類        | ユーザーなしでアクセスを取得 |
| 2    | Microsoft Graph の初期設定 | アプリの登録                 |
| 3    | Microsoft Graph の使い方   | SharePoint, OneDrive         |

### 実行環境

| 環境           | Ver.    |
| :------------- | :------ |
| macOS Catalina | 10.15.6 |
| Python         | 3.7.3   |
| requests       | 2.25.1  |

### ソースコード

実際に実装内容やソースコードを追いながら読むとより理解が深まるかと思います。是非ご活用ください。

[GitHub](https://github.com/nsuhara/python-microsoft-graph-api.git)

### 関連する記事

- [Microsoft Azure Portal](https://azure.microsoft.com/ja-jp/features/azure-portal/)
- [Microsoft Graph ドキュメント](https://docs.microsoft.com/ja-jp/graph/)

## 認証トークン の種類

この記事では `ユーザーなしでアクセスを取得`  の方法をご紹介します。

### ユーザーの代わりにアクセスを取得 ([リンク](https://docs.microsoft.com/ja-jp/graph/auth-v2-user))

- 対話形式でアクセス許可を与える (ログイン認証)
- 利用者側でアプリのアクセスを許可する
- GUIアプリ等で利用

### ユーザーなしでアクセスを取得 ([リンク](https://docs.microsoft.com/ja-jp/graph/auth-v2-service))

- あらかじめ管理者がアクセス許可を与える
- 管理コンソールでアプリのアクセスを許可する
- バッチ処理等で利用

## Microsoft Graph の初期設定

### アプリの登録

1. Microsoft Azure Portal サインイン
2. サブメニュー > Azure Active Directory > アプリの登録 > 新規登録
3. {名前}入力 > 登録

### アクセス権限の設定 (SharePoint と OneDrive)

1. API のアクセス許可 > アクセス許可の追加 > Microsoft Graph > アプリケーションの許可 > `Sites.Read.All` > アクセス許可の追加
2. API のアクセス許可 > アクセス許可の追加 > Microsoft Graph > アプリケーションの許可 > `Files.Read.All` > アクセス許可の追加
3. API のアクセス許可 > {組織名}に管理者の同意を与えます > はい

### クライアント シークレットの設定

1. 新しいクライアント シークレット > 追加 > `値をコピーして保管 (client_secret)`

### クライアントID と テナントID の確認

1. 概要
2. `アプリケーション (クライアント) ID (client_id)`
3. `ディレクトリ (テナント) ID (tennant_id)`

## Microsoft Graph の使い方

### API の初期設定

`{}はご自身の環境に置き換えてください。`

```app/__init__.py
client_id = '{client_id}'
scope = 'https://graph.microsoft.com/.default'
client_secret = '{client_secret}'
grant_type = 'client_credentials'
tennant_id = '{tennant_id}'
graph_url = 'https://graph.microsoft.com/v1.0'
# graph_url = 'https://graph.microsoft.com/beta'
```

### アクセストークン の取得

```app/get_access_token.py
"""curl -d 'client_id={client_id}' \
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
```

### データ の取得 (共通)

```app/graph_api.py
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
```

### SharePoint の取得

```app/get_site_item.py
"""[リスト内のアイテムを列挙する](https://docs.microsoft.com/ja-jp/graph/api/listitem-list?view=graph-rest-1.0&tabs=http)
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

"""サイトアイテム取得
curl -H 'Authorization: Bearer {access_token}' \
-X GET 'https://graph.microsoft.com/v1.0/sites/{siteId}/lists/{list-id}/items?expand=fields'
"""
graph_api(service='/sites/{siteId}/lists/{list-id}/items?expand=fields')

"""サイトアイテム取得(select)
curl -H 'Authorization: Bearer {access_token}' \
-X GET 'https://graph.microsoft.com/v1.0/sites/{siteId}/lists/{list-id}/items?expand=fields(select={key1},{key2})'
"""
graph_api(service='/sites/{siteId}/lists/{list-id}/items?expand=fields(select={key1},{key2})')
```

### OneDrive の取得

```app/get_drive_data.py
"""[DriveItemのコンテンツをダウンロードする](https://docs.microsoft.com/ja-jp/graph/api/driveitem-get-content?view=graph-rest-1.0&tabs=http)
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
```
