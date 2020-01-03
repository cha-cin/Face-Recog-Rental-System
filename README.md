###### tags: `物聯網`
# 人臉辨識之租借系統教學

## 前提!! 請安裝好 Raspberry pi Linux環境 ##
[此為安裝教學連結](https://drive.google.com/file/d/1VUlZtWC8SswSpZoP-LXKf7S2FR2fCVGy/view?usp=sharing)
## 1、**臉部辨識套件安裝**
* Dlib是用於現實世界機器學習和數據分析應用程序的工具包。要安裝dlib，只需在終端中輸入以下命令
```
            sudo pip install dlib
```
* Pillow（也稱為PIL）代表Python Imaging Library，用於打開，操作和保存不同格式的圖像。要安裝PIL，請使用以下命令
```
            sudo pip install pillow
```
* python的face_recognition庫被認為是識別和操作人臉的最簡單的庫。我們將使用該庫來訓練和識別人臉。要安裝此庫，請遵循以下命令
```
            sudo pip3 install face_recognition
```
### 1-1建立臉孔輪廓圖片集目錄
![](https://i.imgur.com/csAXry4.png)
* 上突為專案裡面的Face_Images資料夾應該包含(姓名)子目錄，這些子目錄具有應被識別的人的名字，並且其中包含其的圖片。在此專案我用自己的圖像作為例子。(**每個人名至少需要5張照片**)
### 1-2 Face Trainer Program 訓練臉部模型
* 讓我們看一下Face_Traineer.py程序。該程序的目的是打開Face_Images目錄中的所有圖像並蒐索面部。一旦檢測到面部，它將裁剪面部並將其轉換為灰階，然後轉換為numpy數組。然後我們最終使用我們之前安裝的face_recognition進行訓練並將其保存為名為face- trainner.yml的模型。此模型中的數據以後可以用於識別面部。最後給出了完整的Trainer程序。
* 我們通過導入所需的openCV(cv2)開始該程序。cv2模塊用於圖像處理，numpy用於將圖像轉換為數學表達式，os模塊用於在目錄中導航，而PIL用於處理圖像。
    ```
            import cv2 #For Image processing
            import numpy as np #For converting Images to Numerical array
            import os #To handle directories
            from PIL import Image #Pillow lib for handling images
    ```
* 接下來，我們必須使用(haarcascade_frontalface_default.xml)分類器來檢測圖像中的人臉。務必確保已將此xml文件放置在同目錄文件夾中，否則將遇到錯誤。然後，我們使用識別器變量創建本地二進制模式直方圖（LBPH）人臉識別器。
    ```
            face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
            recognizer = cv2.face.LBPHFaceRecognizer_create()
    ```
* **注意 !! cv2.face** 安裝參考(https://stackoverflow.com/questions/45655699/attributeerror-module-cv2-face-has-no-attribute-createlbphfacerecognizer)
* 然後，我們必須進入Face_Images目錄以訪問其中的圖像
    ```
            Face_Images = os.path.join(os.getcwd(), "Face_Images") #Tell the program where we have saved the face images
    ```
* 然後，我們使用for循環進入Face_Images目錄的每個子目錄，並打開任何以jpeg，jpg或png結尾的文件。每個圖像的路徑存儲在一個名為path的變數中，放置圖像的文件夾名稱（將是該人的名字）存儲在一個名為person_name的變數中。
    ```
    for root, dirs, files in os.walk(Face_Images): #go to the face image directory
        for file in files: #check every directory in it
            if file.endswith("jpeg") or file.endswith("jpg") or file.endswith("png"): #for image files ending with jpeg,jpg or png
                path = os.path.join(root, file)
                person_name = os.path.basename(root)
    ```
* 如果此人的姓名已更改，我們將增加一個名為Face_ID的變量，這將有助於我們為不同的人使用不同的Face_ID，稍後我們將使用它來識別該人的姓名。
    ```
    if pev_person_name!=person_name: #Check if the name of person has changed
        Face_ID=Face_ID+1 #If yes increment the ID count
        pev_person_name = person_name
    ```
* 由於OpenCV使用灰階圖像比使用彩色圖像要容易得多，因為可以忽略BGR值。因此，為了減少圖像中的值，我們將其轉換為灰階，然後還將圖像調整為(550*550)，以使所有圖像保持一致。確保圖像中的臉處於中間位置，否則臉部將被裁剪掉。最後將所有這些圖像轉換為numpy數組，以獲取圖像的數學值。然後使用級聯分類器檢測圖像中的人臉，並將結果存儲在一個名為人臉的變量中。
    ```
    Gery_Image = Image.open(path).convert("L") # convert the image to greysclae using Pillow
    Crop_Image = Gery_Image.resize( (550,550) , Image.ANTIALIAS) #Crop the Grey Image to 550*550 (Make sure your face is in the center in all image)
    Final_Image = np.array(Crop_Image, "uint8")
    faces = face_cascade.detectMultiScale(Final_Image, scaleFactor=1.5, minNeighbors=5) #Detect The face in all sample image
    ```
* 一旦檢測到臉部，我們將裁剪該區域並將其視為我們的關注區域（ROI）。ROI區域將用於訓練面部識別器。我們必須將每個ROI面附加到名為x_train的變數中。然後，我們將此ROI值以及面部ID值提供給識別器，識別器將為我們提供訓練數據。這樣獲得的數據將被保存。
    ```
    for (x,y,w,h) in faces:
        roi = Final_Image[y:y+h, x:x+w] #crop the Region of Interest (ROI)
        x_train.append(roi)
        y_ID.append(Face_ID)

    recognizer.train(x_train, np.array(y_ID)) #Create a Matrix of Training data
    recognizer.save("face-trainner.yml") #Save the matrix as YML file
    ```
* 編譯該程序時，您會發現face-trainner.yml文件每次都會更新。因此，無論何時對Face_Images目錄中的照片進行任何更改，請確保都編譯該程序。編譯後，您將獲得如下所示的人臉ID，路徑名，人名和numpy數組，用於調試目的。
![](https://i.imgur.com/Ygtt5gF.png)
### 1-3 Face Recog Program 就可以開始辨識啦!




### 1-4 租借時間申請網站架構
1. 伺服器(flask)端socket安裝
* 我選擇安裝 python socketio 作為伺服器與客戶端溝通的橋樑。
```
pip3 install socket
```
* 伺服器端原始碼在 app.py 

2. 客戶端安裝
```
pip3 install "python-socketio[client]" 
```
* 客戶端原始碼在 Client_text.py & Face_Recoge.py

### 2-1 NodeMcu & Micro Servo開鎖裝置安裝(後來無法配合專案使用，可略過)

* 我們要使用NodeMcu 連接 客戶端Micro Servo 使其可以連接上網路與伺服器溝通。
* 教學網址:
https://hackmd.io/N1c6-vp3QEexJNSqv63Keg

### 2-2 Micro Servo 馬達控制

* 範例檔:
其中 我用了GPIO 17作為訊號輸出腳位。
* 角度控制: 其中 **ChangeDutyCycle** 就是python 用來控制馬達角度的方法。
* 記住!!! **頻率很重要**
![](https://i.imgur.com/14zyBwl.png)
參考網站:
https://blog.everlearn.tw/%E7%95%B6-python-%E9%81%87%E4%B8%8A-raspberry-pi/raspberry-pi-3-mobel-3-%E5%88%A9%E7%94%A8-pwm-%E6%8E%A7%E5%88%B6%E4%BC%BA%E6%9C%8D%E9%A6%AC%E9%81%94

* 此為範例檔，可以先用來測試馬達能否驅動。
```
servoPIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)


p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz

def control_micro_servo(data):
    global p
    print(data)
    print(type(data))
    if data == "true":
        print("hello")
        p.start(2.5) # Initialization
    try:
        p.ChangeDutyCycle(5)
        time.sleep(0.5)
        p.ChangeDutyCycle(6.25)
        time.sleep(0.5)
        p.ChangeDutyCycle(7.5)
    except KeyboardInterrupt:
        p.stop()
        GPIO.cleanup()
        #GPIO.cleanup()
```
### 專案程式說明:
https://hackmd.io/1SQFnjzITIenGYr4Go2nKw

