// import {RelayServer} from "https://chirimen.org/remote-connection/js/beta/RelayServer.js";
import http from 'http';
import {requestGPIOAccess} from "./node_modules/node-web-gpio/dist/index.js";
const sleep = msec => new Promise(resolve => setTimeout(resolve, msec));



// XXX: This is just debug so that  I use chirimentest channel
// いろんな人とconnectしたい場合、web serverで接続先を指定できるようにする。
// relayserver以外を使うべきか？
// 複数台ある時どうする？→deviceIDをもとに、
// https://chirimen.org/remote-connection/#サービスごとの利用方法
// const channel = RelayServer("chirimentest", "chirimenSocket"); 

// 

async function send_request(is_here) {

    const res = await new Promise((resolve, reject) => {
        try {
          const port = process.env.PORT || '5000'
          const url = `http://192.168.128.106:${port}/send_existence`
          const content = `{"is_here": ${is_here}}`
          const req = http.request(url, { // <1>
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Content-Length': '' + content.length,
              'X-Header': 'X-Header',
            },
          })
    
          req.on('response', resolve) // <2>
          req.on('error', reject) // <3>
          req.write(content) // <4>
          req.end() // <5>
        } catch (err) {
          console.log(err)
          reject(err)
        }
      })
    
}



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
        console.log(ev.value)
        send_request(1)
        // // RelayServerによる通信
        // channel.send({
        //     "status": 1,
        //     "command": "lock",
        //     "direction": -1 // 鍵施錠方向をクラウドで設定したものが格納される場合、ここは、device上では記録されない想定）
        //     // プロトタイプ現時点ではベタ打ちでデモで用いる鍵の施錠方向をセットする
        // })
    } else if (ev.value == 0){
        console.log(ev.value)
        send_request(0)
        // RelayServerによる通信
        // channel.send({
        //     "status": 1,
        //     "command": "lock",
        //     "direction": -1 // 鍵施錠方向をクラウドで設定したものが格納される場合、ここは、device上では記録されない想定）
        //     // プロトタイプ現時点ではベタ打ちでデモで用いる鍵の施錠方向をセットする
        // })
    }
}

async function humanDetect() {
  const gpioAccess = await requestGPIOAccess();
  const port = gpioAccess.ports.get(12);

  await port.export("in");
  port.onchange = detect;

}

humanDetect();