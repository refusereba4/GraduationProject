## 软件功能与使用方法简介(Software function and use method introduction)
从文末的链接中下载权重文件并放入到项目目录中，然后需要搭建环境以及安装需要的库（搭建细节在论文中有介绍），最后在IDE或终端运行MainWindow.py文件即可启动软件，软件包括以下功能:
Download the weight file from the link at the end of the paper and put it into the project directory. Then it is necessary to build the environment and install the required library (the details of the construction are introduced in the paper). Finally, run the MainWindow.py file in the IDE or terminal to start the software, which includes the following functions:

 ### 水果图片分类功能(Fruit picture classification function)
  #### 单图模式(Single picture mode)
单图模式下点击选择图片按钮选择图片，之后点击运行按钮，在已选择图片情况下，系统会调用由train.py训练好的权重文件（相关权重文件过大，可通过下面的网盘链接下载）对图片进行识别，然后返回识别结果，并将结果在界面上进行展示。
In the single image mode, click the "Select picture" button to select the picture, and then click the "Run" button. When the picture has been selected, the system will call the weight file trained by train.py (the relevant weight file is too large, you can download it through the web disk link below) to identify the picture, and then return the recognition result and display the result on the interface.


![](https://github.com/refusereba4/quantumultxrules/blob/main/markdownpic/GraduationProject/16780217544907.jpg?raw=true)

  #### 多图模式(Multi-picture mode)
  多图模式下点击选择文件夹按钮选择待检测图片文件夹，
点击保存结果文件夹选择将识别结果保存到所选择的文件夹下，在两个文件夹已选择的情况下，点击运行按钮系统开始进行批量识别，并返回结果，将结果在页面上进行展示。
In multi-image mode, click the Select folder button to select the image folder to be detected.
Click Save Results folder to save the recognition results to the selected folder. When two folders have been selected, click the Run button to start batch recognition, return the results, and display the results on the page.

![](https://github.com/refusereba4/quantumultxrules/blob/main/markdownpic/GraduationProject/16780052700471.jpg?raw=true)

### 水果图片标注功能(Fruit picture label function)
#### 单图模式(Single picture mode)
单图模式下点击选择图片按钮选择图片，之后点击运行按钮，在已选择图片情况下，系统会调用对应已训练好的模型权重文件对图片进行检测，然后返回结果，并将结果在界面上进行展示。
In the single graph mode, click the "Select picture" button to select the picture, and then click the "Run" button. When the picture has been selected, the system will call the corresponding trained model weight file to detect the picture, and then return the result and display the result on the interface.

#### 多图模式(Multi-picture mode)
多图模式下点击选择文件夹按钮选择待检测图片文件夹，点击保存结果文件夹选择将识别结果保存到那个文件夹下，在两个文件夹已选择的情况下，点击运行按钮系统开始进行批量检测，并返回结果，将结果在页面上进行展示。
In multi-image mode, click the "Select folder" button to select the image folder to be detected, and click "Save Results" folder to select the folder to save the recognition results. When two folders have been selected, click "Run" button to start batch detection, return the results, and display the results on the page.


![](https://github.com/refusereba4/quantumultxrules/blob/main/markdownpic/GraduationProject/16780054901574.jpg?raw=true)

### 实时标注(Label live)
点击开启检测按钮，系统会自动检测机器是否拥有摄像头设备，当拥有摄像头设备后，会开启摄像头，并采集摄像头的实时画面进行标注，并将标注的方框实时显示在画面上。
Click the Open detection button, the system will automatically detect whether the machine has a camera device, when the camera device has, the camera will be turned on, and the real-time picture of the camera will be captured for annotation, and the marked box will be displayed on the screen in real time.


![](https://github.com/refusereba4/quantumultxrules/blob/main/markdownpic/GraduationProject/16780057130804.jpg?raw=true)

![](https://github.com/refusereba4/quantumultxrules/blob/main/markdownpic/GraduationProject/16780057182583.jpg?raw=true)



## 相关权重文件与演示视频下载链接(Relevant weights file and demo video download link)
https://drive.google.com/drive/folders/1hTtBLEywHBLFSAidUaKYBxBh1rscELYY?usp=sharing

yolo_weights.pth
将此文件放到model_data文件夹中
Place this file in the model_data folder


Epoch99-Total_Loss5.0547-Val_Loss6.0223.pth
将此文件放到项目根目录下
Place this file in the project root folder


resNet101.pth
Place this file in the project root folder


