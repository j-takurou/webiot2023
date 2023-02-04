# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time
import json
import urllib.request

# LED_PIN    = 12 # LEDピン番号(BCMの番号)
SWITCH_PIN = 27 # タクトスイッチのピン番号(BCM番号)


# GPIOを扱う準備
def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    # GPIO.setup(LED_PIN, GPIO.OUT)
    # GPIO.setup(SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) # プルアップ
    GPIO.setup(SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # プルダウン

# ピンの状態を読む
def read_pin(pin_number):
    return GPIO.input(pin_number)


def send(data):
    """    data = {
                "status": 1,
                "command": "lock",
                "direction": -1 # 鍵施錠方向をクラウドで設定したものが格納される場合、ここは、device上では記録されない想定）
                # プロトタイプ現時点ではベタ打ちでデモで用いる鍵の施錠方向をセットする
            }
    """
    url = "localhost:hogehoege" # デモではモータサイドのIPaddressを入れる
    headers = {
        'Content-Type': 'application/json',
    }
    # REVIEW: 切り離してテストする
    # 200以外が帰ってきた時エラー通知できるように修正したい
    req = urllib.request.Request(url, json.dumps(data).encode(), headers)
    with urllib.request.urlopen(req) as res:
        body = res.read()

    

def main():
    setup_gpio() # GPIOの準備

    try:
        # 1秒ごとに点灯/消灯を繰り返す
        while(True):
            if read_pin(SWITCH_PIN) == 1: # 在なのでlock
                # http通信でAPIを叩く
                send(data = {"status": 0, "command": "lock","direction": -1 })
            else:
                send(data = {"status": 1, "command": "unlock","direction": -1 })
            time.sleep(10)

    except KeyboardInterrupt:
        # Ctrl+Cで終了した場合、GPIO設定をクリア
        GPIO.cleanup()