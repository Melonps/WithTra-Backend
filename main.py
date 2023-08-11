from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi import FastAPI
from fastapi import HTTPException
import firebase_admin
from pydantic import BaseModel  # リクエストbodyを定義するために必要
from firebase_admin import credentials
from firebase_admin import firestore
from pathlib import Path
from typing import Tuple
import uvicorn
import datetime

app = FastAPI()

origins = ["http://localhost:3000", "http://localhost", "http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
JSON_PATH = "admin-sdk.json"


cred = credentials.Certificate(JSON_PATH)
firebase_admin.initialize_app(cred)
db = firestore.client()


class PostData(BaseModel):
    userid: str
    username: str
    coin: str
    price: int
    comment: str
    tag: list = []
    alignment: str


@app.get("/")
async def get():
    return "Hello World"


@app.get("/get_file/{filename:path}")
async def get_file(filename: str):
    """任意ファイルのダウンロード"""
    current = Path()
    file_path = current / "files" / filename

    response = FileResponse(path=file_path, filename=f"download_{filename}")

    return response


@app.post("/post_trading_record/")
async def post_activity(data: PostData):
    try:
        db.collection("ActivityList").add(
            {
                "userid": data.userid,
                "username": data.username,
                "coin": data.coin,
                "price": data.price,
                "comment": data.comment,
                "tag": data.tag,
                "alignment": data.alignment,
                "datetime": datetime.datetime.now(),
                "up": True,
            }
        )
    except Exception as e:
        print("Error:", e)
        return "エラーが発生しました"
    return "ok"


@app.get("/get_activity_list/{userid}")
async def get_activity_list(userid: str):
    try:
        activity_list = []
        if userid == "all":
            docs = (
                db.collection("ActivityList")
                .order_by("datetime", direction=firestore.Query.DESCENDING)
                .limit(30)
                .get()
            )  # 最大30件を取得
            for doc in docs:
                activity_list.append(doc.to_dict())
            return activity_list
        else:
            docs = (
                db.collection("ActivityList")
                .where("userid", "==", userid)
                .limit(30)
                .get()
            )  # 最大30件を取得
            for doc in docs:
                activity_list.append(doc.to_dict())
            return activity_list

    except Exception as e:
        print("Error in get_activity_list:", e)
        return "エラーが発生しました"


@app.get("/get_summary/{range_start}/{range_end}")
async def get_summary(range_start: int, range_end: int):
    try:
        docs = db.collection("Users").get()
        users_coins_list = []
        for doc in docs:
            doc_data = doc.to_dict()
            if "tag" in doc_data:
                if (
                    doc_data["state"] >= range_start * 10000
                    and doc_data["state"] <= range_end * 10000
                ):
                    users_coins_list.extend(doc_data["tag"])
        crypto_counts = {}
        for crypto in users_coins_list:
            if crypto in crypto_counts:
                crypto_counts[crypto] += 1
            else:
                crypto_counts[crypto] = 1
        response_data = []
        for key, value in crypto_counts.items():
            response_data.extend([{"name": key, "value": value}])
        return response_data
    except Exception as e:
        print("Error in get_summary:", e)
        return "エラーが発生しました"


@app.post("/register_user/")
async def register_user(data: dict):
    try:
        path = f"Users/{data['username']}"
        doc = db.document(path).get()
        if doc.exists:
            print("すでに登録されています")
            return "すでに登録されています"
        else:
            db.collection("Users").document(data["username"]).set(
                {
                    "username": data["username"],
                    "state": data["state"],
                    "target": data["target"],
                    "tag": data["tag"],
                }
            )
            return "ok"
    except Exception as e:
        print("Error:", e)
        return "エラーが発生しました"


@app.post("/create_user/")
async def create_user(data: dict):
    try:
        path = f"Users/{data['userid']}"
        doc = db.document(path).get()
        if doc.exists:
            raise HTTPException(status_code=409, detail="すでに登録されています")
        else:
            print(data["userid"])
            doc_ref = db.collection("Users")
            doc_ref.document(data["userid"]).set(
                {
                    "userid": data["userid"],
                    "state": 0,
                    "target": 0,
                    "tag": ["Beginner"],
                    "username": "Guest",
                    "bio": "Hello, I'm a guest user!",
                }
            )
            return {"message": "ユーザーが正常に作成されました"}
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail="ユーザーの作成中にエラーが発生しました")


@app.get("/get_user/{userid}")
async def get_user(userid: str):
    try:
        doc = db.collection("Users").document(userid).get()
        if doc.exists:
            return doc.to_dict()
        else:
            raise HTTPException(status_code=404, detail="ユーザーが見つかりません")
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail="ユーザーの取得中にエラーが発生しました")


@app.post("/update_user/")
async def update_user(data: dict):
    try:
        doc = db.collection("Users").document(data["userid"]).get()
        if doc.exists:
            db.collection("Users").document(data["userid"]).update(
                {
                    "username": data["username"],
                    "state": data["state"],
                    "target": data["target"],
                    "tag": data["tag"],
                    "bio": data["bio"],
                }
            )
            return {"message": "ユーザーが正常に更新されました"}
        else:
            raise HTTPException(status_code=404, detail="ユーザーが見つかりません")
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail="ユーザーの更新中にエラーが発生しました")
