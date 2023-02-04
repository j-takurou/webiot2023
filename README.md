# Web IoT makers Hackathon



## The Name of Product
``` Sema-Home```
- Semafor + Homeの造語
- 離れた空間で暮らす人に、トイレを占有されて、「まるで同居人がいるかのごとく」感じられるIoTサービス


## Contents in this repository


### sema-sense
    - 人感センサーで親側（トイレ占有する方）の在不在判定を行う
    - 現在利用しているsource code は、detect-human.**js**

### sema-for-key
    - serverへのpollingを5秒に一回行い、モータの回転を制御し鍵の解錠・施錠を実行するためのスクリプト
    - 現在利用しているsource code は、key-controler.**py**

### server

- sema-sense / sema-for-key間、sema-mic / sema-speaker間の通信を制御するサーバ
    - Flask 2.2系で実装
    - `python app.py`で起動

