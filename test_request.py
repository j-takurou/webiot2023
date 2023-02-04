# 動作確認用サンプル post request sender
import urllib.request
import json


headers = {
    'Content-Type': 'application/json',
}
def main():

    req = urllib.request.Request(url, json.dumps(data).encode(), headers)
    with urllib.request.urlopen(req) as res:
        body = res.read()

    with urllib.request.urlopen('http://sema-srv.local:8000/key-polling/') as response:
        data = json.loads(response.read().decode())
        print(data)


if __name__ == "__main__":
    # send_soundの動作確認用サンプル
    url = 'http://sema-srv.local:8000/send_sound/'
    data = {
        'collect-sound': "1",
    }

    pass