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



# @app.route('/')
# def index():

#     # データベースを開く
#     con = get_db()

#     # テーブル「商品一覧」の有無を確認
#     cur = con.execute("select count(*) from sqlite_master where TYPE='table' AND name='商品一覧'")

#     for row in cur:
#         if row[0] == 0:
#             # テーブル「商品一覧」がなければ作成する
#             cur.execute("CREATE TABLE 商品一覧(コード INTEGER PRIMARY KEY, 商品名 STRING, 値段 REAL)")
#             # レコードを作る
#             cur.execute(
#                 """INSERT INTO 商品一覧(コード, 商品名, 値段) 
#                 values(1, '苺のショートケーキ', 350),
#                 (2, 'チョコケーキ', 380),
#                 (3, 'パインケーキ', 380),
#                 (4, 'バニラアイス', 180),
#                 (5, 'チョコアイス', 200),
#                 (6, '紅茶アイス', 180),
#                 (7, 'りんごのアップルパイ', 250),
#                 (8, 'ホットコーヒー', 100),
#                 (9, 'コーラ', 120),
#                 (10, 'オレンジジュース', 120)
#                 """)
#             con.commit()
    
#     # 商品一覧を読み込み
#     cur = con.execute("select * from 商品一覧 order by コード")
#     data = cur.fetchall()
#     con.close()

#     return render_template('index.html', data = data)

# @app.route('/result', methods=["POST"])
# def result_post():
#     # テンプレートから新規登録する商品名と値段を取得
#     name = request.form["name"]
#     price = request.form["price"]

#     # データベースを開く
#     con = get_db()

#     # コードは既に登録されているコードの最大値＋１の値で新規登録を行う
#     cur = con.execute("select MAX(コード) AS max_code from 商品一覧")
#     for row in cur:
#         new_code = row[0] + 1
#     cur.close()

#     # 登録処理
#     sql = "INSERT INTO 商品一覧(コード, 商品名, 値段)values({},'{}',{})".format(new_code, name, price)
#     con.execute(sql)
#     con.commit()

#     # 一覧再読み込み
#     cur = con.execute("select * from 商品一覧 order by コード")
#     data = cur.fetchall()
#     con.close()

#     return render_template('index.html', data = data)


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
    # import pdb;pdb.set_trace()
    print("arrived")
    data = request.get_data()
    is_here = data["is_here"]

    query = f" UPDATE sema_sense SET is_here={is_here} WHERE device_id = 1"
    con.execute(query)

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



if __name__ == '__main__':
    
    init_db(con)
    app.debug = True
    app.run(host='127.0.0.1', port=8888)

    # server側: 192.168.128.106
