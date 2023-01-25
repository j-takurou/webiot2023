import {requestGPIOAccess} from "./node_modules/node-web-gpio/dist/index.js";
const sleep = msec => new Promise(resolve => setTimeout(resolve, msec));

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
}

async function humanDetect() {
  const gpioAccess = await requestGPIOAccess();
  const port = gpioAccess.ports.get(5);

  await port.export("in");
  port.onchange = detect;

}




