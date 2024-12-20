import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

subdomain = os.getenv("SUBDOMAIN")
app_id = os.getenv("APP_ID")
api_token = os.getenv("API_TOKEN")

url = f"https://{subdomain}.cybozu.com/k/v1/record.json"
file_upload_url = f"https://{subdomain}.cybozu.com/k/v1/file.json"

# headers = {"X-Cybozu-API-Token": api_token, "Content-Type": "application/json"}
# headers = {"X-Cybozu-API-Token": api_token, "Content-Type": "multipart/form-data"}
headers = {"X-Cybozu-API-Token": api_token}

koumoku1 = input("項目１を入力してください：")
koumoku2 = input("項目２を入力してください：")
koumoku3 = input("項目３を入力してください：")

# 添付ファイルをアップロードする
file_path = "pokemon_logo.png"
with open(file_path, "rb") as file:
    files = {'file': (file_path, file)}
    file_response = requests.post(file_upload_url, headers=headers, files=files)

if file_response.status_code == 200:
    # レスポンスからファイルキーを取得
    file_key = file_response.json().get("fileKey")
    print(f"ファイルが正常にアップロードされました。ファイルキー: {file_key}")
else:
    print("ファイルのアップロードに失敗しました。", file_response.status_code)
    print(file_response.json())  # ファイルのレスポンスを表示
    exit()

headers = {"X-Cybozu-API-Token": api_token, "Content-Type": "application/json"}
data = {
    "app": app_id,
    "record": {
        "項目1行目": {"value": koumoku1},
        "項目2行目": {"value": koumoku2},
        "項目3行目": {"value": koumoku3},
        "添付ファイル": {"value": [{"fileKey": file_key}]},
        "選択肢": {"value": "選択肢3"},

    },
}

response = requests.post(url, headers=headers, data=json.dumps(data))

if response.status_code == 200:
    print("データが正常に追加されました")
else:
    print(response.json())  # ファイルのレスポンスを表示
    print("エラーが発生しました", response.status_code)
