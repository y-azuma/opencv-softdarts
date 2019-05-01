
# Opencv-Softdarts
----------
家庭用ダーツボード、ダーツライブゼロに対しopencvを用いてダーツの矢を認識し、BULLに対しスコア計算機能や得点時のサウンド演出といった様々な機能を付け加えます。



## Description
-----------
ダーツボードに矢が刺さった時の音に反応しraspberrypiがダーツボードの写真を撮り、opencvで画像処理、色認識をします。そこから得られた情報から、矢がBULLに刺さっているかどうかを読み取り、得点機能、サウンド演出、アワードムービー演出を行います。
ここでは画像処理によって得られた情報をsocket通信によりraspberrypiからmacに送信し、mac側で作られたguiに反映する方法と、vncによりmacでraspberrypiの画面を映しだし、raspberrypi上で作られたguiに反映する方法の２つを載せました。



## Demo
------------
#### 撮った画像に対してopencvを用いて色認識を行います。
![代替テキスト](https://github.com/y-azuma/opencv-softdarts/blob/master/images/darts_image.jpg?raw=true)


#### 実行した際のgif動画です。
![代替テキスト](https://github.com/y-azuma/opencv-softdarts/blob/master/images/Darts_Demo.gif?raw=true)


#### guiのgif動画です。
![代替テキスト](https://github.com/y-azuma/opencv-softdarts/blob/master/images/darts_demo_gui.gif?raw=true)



## Requirement
------------
python3 または　python2(raspberrypiは初期設定上python2で実行しています。)



## Usage
------------
### 1. socket通信により、mac上で作られたguiを使用する場合

+ darts_socketフォルダのdarts_serverをmac側にdarts_clientをraspberrypi側にダウンロード


+ 以下をmacターミナル上で入力し、display.pyを実行。

     ```$ cd darts_server ```

     ```$ python display.py ```
     
     
+ raspberrypiをssh接続する。以下をraspberrypiターミナル上で入力し、raspi_socket.pyを実行。

     ```$ cd darts_client ```

     ```$ python2 raspi_socket.py ```
     
     
+ gui上でSTARTをクリックするとraspberrypiがダーツ音に反応しカメラを撮るようになります。
![代替テキスト](https://github.com/y-azuma/opencv-softdarts/blob/master/images/gui_image.png?raw=true)


### 2. vncにより、raspberrypi上で作られたguiを使用する場合

+ dartsフォルダをraspberrypiにダウンロード。


+ raspberrypiにx11vncを導入。


+ 以下をraspberrypiターミナル上で入力し、x11vncを実行。

     ```$ x11vnc -usepw -forever```
　　　

+ vncサーバーを起動した上で、以下をraspberryターミナル上で入力し、display.pyを実行。

     ```$ cd darts ```

     ```$ python2 display.py ```
     
     
+ gui上でSTARTをクリックするとraspberrypiがダーツ音に反応しカメラを撮るようになります。
     
     
### - BULL範囲、色認識の調整
#### raspberrypiが撮った画像をBULL範囲に切り取ります。

+ imageprocessor.pyを開き、ImageProcessor関数のimage_scanメソッド内の#frameに画像を入れて切り抜きの部分の数値を調整して撮った画像がBULL範囲に切り取られるようにします。


#### 色認識でダーツ矢を認識するため、チップの色をを調べプログラムに反映する必要があります。（ボードの色上、ダーツチップは緑であると正確に認識してくれます。）

+ 撮った画像を[こちらのサイト](https://www.peko-step.com/tool/getcolor.html)を使ってダーツのチップの色（RGB)を調べます。


+ imageprocessor.pyを開き、ImageProcessor関数のimage_scanメソッド内の＃色検出のlower（最小値）upper（最大値）の数値を先ほど調べたチップの色を参考に調整します。lowerとupperの間の色が検出されるようになります。ここでの数値はRGBではなく、BGRの順番であることに注意してください。



# License
-------------
MIT











