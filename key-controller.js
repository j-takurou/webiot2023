import {RelayServer} from "https://chirimen.org/remote-connection/js/beta/RelayServer.js";
const { requestI2CAccess } = require("node-web-i2c");
const PCA9685 = require("@chirimen/pca9685");
const { promisify } = require("util");
const sleep = promisify(setTimeout);



main();

function parse_socket(msg){
    data = msg.data
    status = data["status"]
    command = data["command"]
    direction = data["direction"]
    return status, command, direction
}


async function main(msg) {
    /* 
        子（クライドサーバ）からの信号を待ち、websocketで受け取る
     */
  //TODO: 施錠制御・解錠制御ごとにsubscription channelを分けられるか？
  const i2cAccess = await requestI2CAccess();
  const port = i2cAccess.ports.get(1);
  const pca9685 = new PCA9685(port, 0x40);
  // servo setting for sg90
  // Servo PWM pulse: min=0.0011[sec], max=0.0019[sec] angle=+-60[deg]
  status, direction = parse_socket(msg);
  km = KeyMotor(status, command, direction, pca9685);
  km.execute()
}



class KeyMotor {
    constructor(status, command, direction, pwm_driver){
        this.direction = direction // locking方向が時計回り→0, 反時計回り→1
        this.command = command
        this.status = status// 1, if locked else 0
        this.pwm_driver = pwm_driver
    }
    async init(){
        await this.pwm_driver.init(0.001, 0.002, 30);
    }
    
    async turn(to_lock){
        direction_str = (this.direction == 1) ? "反時計回り" : "時計回り";
        console.log(`rotate to ${direction_str}`);
        // 施錠方向設定を確認
        // 時計回りに施錠？ →angle +
        // 反時計回りに施錠？→angle -
        await this.pwm_driver.setServo(0, 90 * this.direction * to_lock);
    }
    lock(){
        turn(to_lock=1);
    }
    unlock(){
        turn(to_lock=0);
    }

    execute(){
        if (this.command == "unlock" ){
            this.unlock()
        }
        else {
            this.lock()
        }
    }
}

// XXX: This is just debug so that  I use chirimentest channel
// いろんな人とconnectしたい場合、web serverで接続先を指定できるようにする。
// relayserver以外を使うべきか？
// 複数台ある時どうする？→deviceIDをもとに、
// https://chirimen.org/remote-connection/#サービスごとの利用方法
const channel = RelayServer("chirimentest", "chirimenSocket"); 

// 
channel.onmessage = main

