import {RelayServer} from "https://chirimen.org/remote-connection/js/beta/RelayServer.js";
import {requestGPIOAccess} from "./node_modules/node-web-gpio/dist/index.js";
const sleep = msec => new Promise(resolve => setTimeout(resolve, msec));



// XXX: This is just debug so that  I use chirimentest channel
// いろんな人とconnectしたい場合、web serverで接続先を指定できるようにする。
// relayserver以外を使うべきか？
// 複数台ある時どうする？→deviceIDをもとに、
// https://chirimen.org/remote-connection/#サービスごとの利用方法
const channel = RelayServer("chirimentest", "chirimenSocket"); 

// 



function detect(ev){
    /* 
    port.onchange で呼び出すcallback function
    Args:
         ev.value: [0, 1]
         TODO: 0,1どっちがどっちだったか、確認
    Returns:
        if value = x: (人を検知)
            device_idと共に、人がいることをweb serverにpush通知を出す。
            TODO: 通知は AJAX通信/websocketを想定
        else:
            device_idと共に、人がいなくなったことをweb serverにpush通知を出す。
            TODO: 通知は AJAX通信/websocketを想定

    */ 
    // Pull Upを想定しているので、「在」
    if (ev.value == 1){
        // RelayServerによる通信
        channel.send({
            "status": 1,
            "command": "lock",
            "direction": -1 // 鍵施錠方向をクラウドで設定したものが格納される場合、ここは、device上では記録されない想定）
            // プロトタイプ現時点ではベタ打ちでデモで用いる鍵の施錠方向をセットする
        })
    } else if (ev.value == 0){
        // RelayServerによる通信
        channel.send({
            "status": 1,
            "command": "lock",
            "direction": -1 // 鍵施錠方向をクラウドで設定したものが格納される場合、ここは、device上では記録されない想定）
            // プロトタイプ現時点ではベタ打ちでデモで用いる鍵の施錠方向をセットする
        })
    }
}

async function humanDetect() {
  const gpioAccess = await requestGPIOAccess();
  const port = gpioAccess.ports.get(5);

  await port.export("in");
  port.onchange = detect;

}




