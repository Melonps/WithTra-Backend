import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import datetime


def main():
    # ===================== Firebase =====================================
    # このPythonファイルと同じ階層に認証ファイルを配置して、ファイル名を格納
    JSON_PATH = "admin-sdk.json"

    # Firebase初期化
    cred = credentials.Certificate(JSON_PATH)
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    dt_now = datetime.datetime.now()
    try:
        doc_ref = db.collection("news")
        doc_ref.add(
            {
                "title": "hello world",
                "date": dt_now.strftime("%Y年%m月%d日"),
            }
        )
    except:
        print("error")


if __name__ == "__main__":
    main()
