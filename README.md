# GitHub Repository Inspector

このアプリケーションは、指定したGitHubリポジトリのファイル構造と各ファイルのrawページのURLを取得し、整形して出力します。また、リポジトリの現在のコミット数も取得することができます。

## 準備
1. `.env`ファイルをプロジェクトのルートディレクトリに作成し、以下のように設定してください。
```plaintext
OWNER=<リポジトリのオーナー名>
REPO=<リポジトリ名>
TOKEN=<GitHubのPersonal Access Token>
```

2. ファイルのurl（rawページ）を取得する場合、`main.py`ファイルの変数target_extensionで拡張子をフィルタリングできます