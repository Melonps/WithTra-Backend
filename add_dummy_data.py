import firebase_admin
from pydantic import BaseModel  # リクエストbodyを定義するために必要
from firebase_admin import credentials
from firebase_admin import firestore
import datetime
import requests
import json
import string
import random
import time

JSON_PATH = "admin-sdk.json"

cred = credentials.Certificate(JSON_PATH)
firebase_admin.initialize_app(cred)
db = firestore.client()

tag_list_record = [
    "Short Term",
    "Mid Term",
    "Long Term",
    "Profit",
    "Loss",
    "Add",
    "Withdraw",
    "First Trade",
    "Last Trade",
    "New Coin",
    "New Exchange",
    "New Wallet",
    "New Strategy",
    "New Indicator",
    "New Bot",
    "New Algorithm",
    "New Project",
    "New Token",
    "New NFT",
    "New DeFi",
    "New DEX",
    "New DAO",
    "New Yield Farming",
    "Hedge",
    "Leverage",
    "Margin",
    "Futures",
    "Options",
    "ETF",
    "Stock",
    "Forex",
    "Commodity",
    "Derivatives",
    "Staking",
]

tag_list_coin = [
    "Bitcoin (BTC)",
    "Ethereum (ETH)",
    "Binance Coin (BNB)",
    "Cardano (ADA)",
    "Solana (SOL)",
    "XRP (XRP)",
    "Polkadot (DOT)",
    "Dogecoin (DOGE)",
    "Litecoin (LTC)",
    "Chainlink (LINK)",
    "Stellar (XLM)",
    "Bitcoin Cash (BCH)",
    "Tether (USDT)",
    "USD Coin (USDC)",
    "VeChain (VET)",
    "Uniswap (UNI)",
    "Aave (AAVE)",
    "Polygon (MATIC)",
    "Cosmos (ATOM)",
    "Tezos (XTZ)",
]


def add_trading_record(record_data):
    try:
        db.collection("ActivityList").add(
            {
                "username": record_data["username"],
                "coin": record_data["coin"],
                "alignment": record_data["alignment"],
                "userid": record_data["userid"],
                "up": record_data["up"],
                "price": record_data["price"],
                "comment": record_data["comment"],
                "tag": record_data["tag"],
                "datetime": datetime.datetime.now(),
            }
        )
    except Exception as e:
        print("エラー:", e)
        return "エラーが発生しました"
    return "ok"


def create_profile(user_data):
    try:
        db.collection("Users").add(
            {
                "username": user_data["username"],
                "userid": user_data["userid"],
                "state": user_data["state"],
                "target": user_data["target"],
                "tag": user_data["tag"],
            }
        )
    except Exception as e:
        print("エラー:", e)
        return "エラーが発生しました"
    return "ok"


def get_random_username():
    try:
        response = requests.get("https://randomuser.me/api/")
        data = response.json()
        results = data.get("results")
        if results:
            user = results[0].get("name")
            first_name = user.get("first")
            return first_name
        else:
            return "Guest"
    except Exception as e:
        print("エラー:", e)
        return "Guest"


def get_random_last_name():
    try:
        response = requests.get(
            "https://green.adam.ne.jp/roomazi/cgi-bin/randomname.cgi?n=1"
        )
        response_text = response.text
        # "callback(" と ");" を除去してJSON形式の文字列にする
        json_data_str = response_text.replace("callback(", "").replace(")", "")
        # JSON文字列を辞書に変換
        data = json.loads(json_data_str)

        results = data.get("name")
        print(results)
        if results:
            full_name = results[0][0]
            last_name = full_name.split(" ")[1]
            return last_name
        else:
            return get_random_username()
    except Exception as e:
        print("エラー:", e)
        return get_random_username()


def randomname(n):
    randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
    return "".join(randlst)


def generate_random_user():
    while True:
        for _ in range(2):
            num_selections = 4
            random_selections = random.sample(tag_list_coin, num_selections)
            random_state = random.randint(0, 1000) * 10000
            random_goal = random.randint(200, 10000) * 10000
            user_data = {
                "username": get_random_username(),
                "state": random_state,
                "target": random_goal,
                "tag": random_selections,
            }
            create_profile(user_data)
            print(user_data)
        print("User created")
        time.sleep(1)


def generate_random_record():
    while True:
        for i in range(1):
            random_selections = random.sample(tag_list_coin, 1)
            random_price = random.randint(1, 50) * 1000
            random_comment = "Hello"
            random_tag = random.sample(tag_list_record, 2)
            record_data = {
                "username": get_random_last_name(),
                "userid": randomname(4),
                "coin": random_selections[0],
                "price": random_price,
                "comment": random_comment,
                "tag": random_tag,
                "up": True,
                "alignment": "buy",
                "datetime": datetime.datetime.now(),
            }
            add_trading_record(record_data)
        print("User created", record_data)
        time.sleep(4)


# generate_random_user()
generate_random_record()
