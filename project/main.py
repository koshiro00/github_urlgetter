import requests
import dotenv
import os
import pyperclip
import datetime
import webview

# ◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️
# 関数一覧
# ◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️
# 出力形式の整形
def print_tree(items, prefix="", log_file=None):
    for i, item in enumerate(items):
        is_last = i == len(items) - 1
        # ディレクトリの場合
        if "children" in item:  
            line = f"{prefix}{'└── ' if is_last else '├── '}{os.path.basename(item['path'])}\n"
            if log_file:
                log_file.write(line)
            new_prefix = f"{prefix}{'    ' if is_last else '│   '}"
            print_tree(item["children"], new_prefix, log_file)
        # ファイルの場合
        else:  
            if item["path"].endswith(
                (".html", ".js", ".ts", ".jsx", ".tsx", ".prisma", ".json", ".css", ".scss", ".py", ".md", ".spec")
            ):
                line = f"{prefix}{'└── ' if is_last else '├── '}{os.path.basename(item['path'])} -> {item['url']}\n"
            else:
                line = f"{prefix}{'└── ' if is_last else '├── '}{os.path.basename(item['path'])}\n"
            if log_file:
                log_file.write(line)

# リポジトリ一覧を取得
def get_repositories(token):
    url = f"https://api.github.com/user/repos"  # changed endpoint
    headers = {"Authorization": f"token {token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    repos = [repo["name"] for repo in response.json()]
    return repos

# リポジトリ詳細を取得
def get_repository_info(repo_name):
    repo_info = {}
    url = f"https://api.github.com/repos/{owner}/{repo_name}"
    headers = {"Authorization": f"token {token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    repo_data = response.json()
    repo_info["name"] = repo_data["name"]
    repo_info["lastCommitDate"] = repo_data["pushed_at"]
    repo_info["isPublic"] = not repo_data["private"]
    return repo_info

# リポジトリから現在のコミット数を取得
def get_commit_count(owner, repo, token):
    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    headers = {"Authorization": f"token {token}"}
    params = {"per_page": 1}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return int(response.headers["Link"].split(",")[1].split("&page=")[1].split(">")[0])


# リポジトリからrawページのURLを取得する関数
def get_raw_urls(owner, repo, token, path="", current_tree=None):
    base_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {token}", 
    }
    response = requests.get(base_url, headers=headers)
    response.raise_for_status()

    if current_tree is None:
        current_tree = {"path": "", "children": []}  # 格納用配列

    # レスポンスをループ
    for item in response.json():  
        # ファイルの場合
        if item["type"] == "file":  
            raw_url = item["download_url"]  # rawページURLを取得
            file_path = item["path"]  # ファイルパスを取得
            current_tree["children"].append({"url": raw_url, "path": file_path})
        # アイテムがディレクトリの場合
        elif item["type"] == "dir":  
            subdir_tree = {"path": item["path"], "children": []}
            current_tree["children"].append(subdir_tree)
            get_raw_urls(owner, repo, token, item["path"], subdir_tree)  # 再帰的にディレクトリ内のURLを取得
            
    return current_tree


# ◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️
# 変数
# ◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️
dotenv.load_dotenv()
owner = os.getenv("OWNER")
token = os.getenv("TOKEN")
os_username = os.getenv("USERNAME")

# 時間
t_delta = datetime.timedelta(hours=9)
JST = datetime.timezone(t_delta, "JST")
now = datetime.datetime.now(JST)
date = now.strftime("%Y/%m/%d %I:%M(%p)")  # 例) 2021/11/04 05:37(PM)

# ◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️
# 実行
# ◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️

# apiとしてwinow(html)から使えるように公開
if __name__ == "__main__":

    class Api:
        def get_repositories(self):
            return get_repositories(token)

        def get_repository_info(self, repo_name):
            return get_repository_info(repo_name)

        def submit(self, data):
            # データを取得
            repo = data["repo"]
            commit_count = get_commit_count(owner, repo, token)

            # ログファイルのパス
            file_path = f"/Users/{os_username}/Downloads/ツール/github_urlgetter/output_repository/{repo}.txt"

            # ファイルが存在しない場合は新しく作成
            if not os.path.isfile(file_path):
                with open(file=file_path, mode="w") as f:
                    pass

            # 書き込みモードで開く
            with open(file_path, "w") as log_file:
                log_file.write(f"実行日: {date}\nリポジトリ: {repo}、現在コミット数: {commit_count}\n\nProject\n")

                urls = get_raw_urls(owner, repo, token)
                print_tree(urls["children"], prefix="", log_file=log_file)

            # 読み取りモードで開いて内容をクリップボードにコピー
            with open(file_path, "r") as result_file:
                result = result_file.read()
                pyperclip.copy(result)

            window.destroy()

    api = Api()
    window = webview.create_window(
        "GitHubリポジトリ情報入力",
        "index.html",
        js_api=api,
        frameless=True,
        easy_drag=True,
        width=300,
        height=500,
    )
    webview.start(http_server=True, debug=True)
