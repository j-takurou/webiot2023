import sqlite3
from flask import Flask,render_template,request,g
from flask import request
from flask import jsonify
import json


app = Flask(__name__)


def get_db():
    # データベースをオープンしてFlaskのグローバル変数に保存
    db = sqlite3.connect('semafor.db')
    return db

con = get_db()

def init_db(connection):
    try:
        q = "CREATE TABLE sema_sense (device_id integer, is_here integer)"
        connection.execute(q)
        connection.execute("INSERT INTO sema_sense VALUES (1, 0)")
        connection.commit()
    except Exception as e:
        print(e)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/rotate/")
def rotate():
    if request.method == "POST":
        data = request.get_data()
        status = data["status"] # close or open
        command = data["command"] # lock or unlock
        direction = data["direction"]
        # Servo = SG90_92R_Class(Pin=4,ZeroOffsetDuty=0)
        # 回転方向を保証できるかどうかが怖い
        # Servo.SetPos(45)
    return "<p>rotate!</p>"


@app.route('/send_existence', methods=["GET", "POST"])
def send_existence():
    """ 
    sema-sense(人感センサ)から送られてくる在不在情報を捌くAPI 
    Method: GET
    """
    data = json.loads(request.get_data().decode())
    is_here = data["is_here"]

    query = f"UPDATE sema_sense SET is_here={is_here} WHERE device_id = 1"
    con.execute(query)
    con.commit()

    return jsonify({'message': 'successfully sent existence data'}), 200

    


@app.route("/key-polling/")
def exist_restroom():

    # sema-senseの最新判定を引っ張ってくる
    if request.method == "GET":
        query = "SELECT is_here FROM sema_sense WHERE device_id = 1"
        res:list = con.execute(query)
        if len(res) == 1:
            is_here = res[0]
        else:
            raise Exception("Device should be identified")

        # dictで返したい

    return json.dumps({"is_here": is_here})


@app.route("/send_sound/", method=["POST"])
def receive_sound():
    """ 
    mic to server
    POC demoでは、micから取れるサウンドデータが、何に関するサウンドかの情報を送信する
    - サウンドが送信されたタイミングでcacheする
    - 10秒でexpireするように設定する。
    """
    import redis
    if request.method == "POST":
        r = redis.Redis(host='localhost', port=6379, db=0)
        # extract sound info
        data = json.loads(request.get_data().decode())
        sound = data["collect-sound"]
        r.set("mic", sound, ex=10)


@app.route("/mic-state/")
def check_sound():
    import redis
    r = redis.Redis(host='localhost', port=6379, db=0)
    with_sound = r.get("mic")

    return str(with_sound) if with_sound is not None else "0"

if __name__ == '__main__':
    
    init_db(con)
    app.debug = True
    app.run(host='0.0.0.0', port=8000)

    # server側: 192.168.128.106
