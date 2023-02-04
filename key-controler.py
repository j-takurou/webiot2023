# 
import urllib.request
import json
try:
    from sg90_sg92 import SG90_92R_Class
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except ModuleNotFoundError:
    pass
import time

def main():
    """
    - serverへのpollingを行う 1 request/5 sec
    - 在である(is_here == 1)ならば、施錠する
        - Notice: 解錠時はpositionが0になるように調整しておく
        - ちょうど90度プロペラを回転させて施錠する
    - 不在(is_here == 0)になったら、解錠する
    """
    try:
        servo = SG90_92R_Class(Pin=4,ZeroOffsetDuty=0)
        servo.SetPos(0)
        while True:
            with urllib.request.urlopen('http://sema-srv.local:8000/key-polling/') as response:
                data = json.loads(response.read().decode())
                print(data)
                if data["is_here"] == 1:
                    # 施錠
                    servo.SetPos(90)
                else:
                    # 解錠
                    servo.SetPos(0)
            time.sleep(5)
    except KeyboardInterrupt:
        servo.Cleanup()
        GPIO.cleanup()

        

if __name__ == "__main__":
    main()