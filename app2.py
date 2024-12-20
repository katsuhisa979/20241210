from flask import Flask, render_template, request, Response, jsonify

import matplotlib.pyplot as plt
import matplotlib, japanize_matplotlib
from io import BytesIO

matplotlib.use("Agg")

app = Flask(__name__)


import requests
import json
from dotenv import load_dotenv
import os
subdomain = os.getenv("SUBDOMAIN")
app_id = os.getenv("APP_ID")
api_token = os.getenv("API_TOKEN")



@app.route("/", methods=["GET", "POST"])
def index():
    
    if request.method == "GET":
        return render_template("index.html")
    
    else:
        koumoku1 = request.form["koumoku1"]
        koumoku2 = request.form["koumoku2"]
        koumoku3 = request.form["koumoku3"]
        url = f"https://{subdomain}.cybozu.com/k/v1/record.json"
        response = requests.get(url)
        headers = {"X-Cybozu-API-Token": api_token, "Content-Type": "application/json"}
        data = {
            "app": app_id,
            "record": {
                "項目1行目": {"value": koumoku1},
                "項目2行目": {"value": koumoku2},
                "項目3行目": {"value": koumoku3},
                # "添付ファイル": {"value": [{"fileKey": file_key}]},
                # "選択肢": {"value": "選択肢3"},
            },
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            print("データが正常に追加されました")
        else:
            print(response.json())  # ファイルのレスポンスを表示
            print("エラーが発生しました", response.status_code)
        return render_template("index.html")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
