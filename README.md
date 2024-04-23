# GitHub Repository Inspector
このアプリケーションは、GitHubリポジトリの構造を視覚的に理解しやすくするためのツールです。
指定されたリポジトリのファイル構造と各ファイルへの直接アクセスリンクを提供し、リポジトリのコミット数も表示します。
これにより、プロジェクトの現状を迅速に把握することが可能になります。

## 機能
- GitHubリポジトリのファイル構造の表示
- ファイルのRaw URLへの直接リンクの提供
- リポジトリの総コミット数の取得

## 使用方法
必要な依存関係をインストールします。
```bash
pip install -r requirements.txt
```

.env ファイルに必要な情報を記入し、main.py を実行します。
```bash
python main.py
```

## UIの例
以下は、このアプリケーションのユーザーインターフェースの一例です。ユーザーはこの画面からリポジトリを選択し、詳細を閲覧することができます。
<img width="494" alt="スクリーンショット 2024-04-23 10 15 46" src="https://github.com/koshiro00/github_urlgetter/assets/130426310/6ed02849-5509-49f5-a7c2-a415f2898d30">


## 設定
- USERNAME: OSにログインしているユーザー名を指定します。
- OWNER: GitHubリポジトリのオーナー名を指定します。
- TOKEN: GitHubのPersonal Access Tokenを設定します。このトークンはリポジトリへのアクセス権限を持つ必要があります。

## 貢献
是非プルリクエストやイシューを通じてご参加ください🙇‍♂️
