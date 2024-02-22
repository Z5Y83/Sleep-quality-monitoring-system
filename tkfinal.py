from cProfile import label
from email.mime import image
from turtle import update
import os
import cv2
import sys
import time
import random
import serial
import pyaudio
import librosa
import datetime
import argparse
import numpy as np
import tkinter as tk
import seaborn as sns
import multiprocessing
from sys import platform
from ctypes import resize
from PIL import Image,ImageTk
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model 
from matplotlib.animation import FuncAnimation 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.metrics import classification_report, confusion_matrix
from tensorflow.keras.layers import Dense, Dropout, Conv1D, MaxPooling1D, Flatten

def determine(age, gender, blood_pressure, BMI_value, waistline_value, breath_value, tired):
    counter = 0

    if age >= 50:
        counter += 1

    if gender == 'man':
        counter += 1

    if blood_pressure == 'yes':
        counter += 1

    if BMI_value > 35:
        counter += 1

    if waistline_value == 'yes':
        counter += 1

    if breath_value == 'yes':
        counter += 1

    if tired == 'yes':
        counter += 1

    print(counter)

    if counter <= 2:
        return '低度風險'

    if counter <= 4:
        return '中度風險'

    if counter > 4:
        return '高度風險'

#聲音辨識
def create_matplotlib_animation(root):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    duration = 5
    fixed_length=94
    model = load_model('C:/openpose-master/openpose-master/build/examples/tutorial_api_python/best.keras')

    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

    fig, ax = plt.subplots()
    line, = ax.plot([], [], lw=2)
    ax.set_ylim(-20000, 20000)
    ax.set_xlim(0, duration)
    ax.set_ylabel("Amplitude")
    ax.set_xlabel("Time")
    class_names = ['nonsnoring', 'snoring']

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack()

    audio_data = np.array([], dtype=np.int16)
    x_data = np.linspace(0, duration, len(audio_data))

    def init():
        line.set_data([], [])
        return line,

    def animate(i):
        data = stream.read(CHUNK)
        new_data = np.frombuffer(data, dtype=np.int16)

        nonlocal audio_data, x_data  # 使用nonlocal关键字来引用外部作用域中的变量
        audio_data = np.concatenate((audio_data, new_data))
        x_data = np.linspace(0, duration, len(audio_data))

        line.set_data(x_data, audio_data)

        if len(audio_data) >= fixed_length:
            audio_segment = audio_data[-fixed_length:]

            # 音频数据进行规范化
            audio_segment_normalized = librosa.util.normalize(audio_segment.astype(np.float32))

            mfcc = librosa.feature.mfcc(y=audio_segment_normalized, sr=RATE, n_mfcc=20)
            mfcc_fixed = librosa.util.fix_length(mfcc, size=fixed_length, axis=1)
            mfcc_input = np.expand_dims(mfcc_fixed, axis=0)  # 添加批次维度

            # 预测
            prediction = model.predict(mfcc_input)
            predicted_class = np.argmax(prediction)

            # 显示结果
            # print(f"Predicted Class: {class_names[predicted_class]}")
            ax.set_title(class_names[predicted_class])

        return line,

    ani = FuncAnimation(fig, animate, init_func=init, frames=50, interval=100)

    time.sleep(1)

    return ani  # 返回动画对象

class SerialReaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SpO2:")

        # 创建一个 Label 用于显示串口数据
        self.serial_data_label = tk.Label(root, text="", font='10')
        self.serial_data_label.pack(pady=20)

        # 打开串口
        self.ser = serial.Serial('COM3', 9600, timeout=1)

        # 启动更新函数
        self.update_serial_data()

    def update_serial_data(self):
        # 从串口读取数据
        data = self.ser.readline().decode().strip()

        # 更新 Label 的文本
        self.serial_data_label.config(text=f"血氧: {data}")

        # 通过 after 方法设置下一个更新
        self.root.after(500, self.update_serial_data)  # 每1000毫秒（1秒）更新一次

    def run(self):
        self.root.mainloop()

# a=datetime.now()+datetime.timedelta(seconds=-1).strftime("%Y%m%d_%H%M%S")
class MyApp:
    def __init__(self, root):
        self.root = root
        # self.root.title("Real-time Image Display")
        
        # 创建一个标签用于显示图像
        self.img_label = tk.Label(root, width=300, height=400)
        self.img_label.pack(side='left')
        
        # 初始图像索引
        # self.a=datetime.now()+datetime.timedelta(seconds=-1).strftime("%Y%m%d_%H%M%S")
        self.i = 232113
        
        # 启动定时器来更新图像
        self.update_image()

    def update_image(self):
        # 打开图像文件
        # img = Image.open('D:/openpose/build/examples/tutorial_api_python/tt/' + str(datetime.datetime.now().strftime("%Y%m%d_%H%M%S")+datetime.timedelta(seconds=-1)) + '.jpg')
        # img = Image.open('D:/openpose/build/examples/tutorial_api_python/tt/20231114_' +str(self.i) + '.jpg')
        img = Image.open('C:/openpose-master/openpose-master/build/examples/tutorial_api_python/tt/tt2/' +str(self.i) + '.jpg')
        img=img.resize((300,400))
        img = ImageTk.PhotoImage(img)

        # 更新图像标签的图像
        self.img_label.config(image=img)
        self.img_label.image = img

        self.i += 1

        # 设置下一个更新
        self.root.after(500, self.update_image)  # 每500毫秒 (0.5秒) 更新一次图像

class FirstPage(object):
    def __init__(self, master=None):
        self.window = master
        self.startLabel=tk.Label(self.window,text='睡眠品質偵查系統',font=('Arial',50,'bold')).pack()
        self.startLabel_en=tk.Label(self.window,text='Sleep quality monitoring system',font=('Arial',30,'bold')).pack()
        #背景圖片
        self.img_background=Image.open('C:/openpose-master/openpose-master/build/examples/tutorial_api_python/firstpage.png')
        self.img_background=self.img_background.resize((640,300))
        self.tk_img_background=ImageTk.PhotoImage(self.img_background)
        self.canvas=tk.Canvas(self.window,width=640,height=200).pack()
        self.backgroundLabel=tk.Label(self.canvas,image=self.tk_img_background,width=640,height=200)
        self.backgroundLabel.pack(side='top')

        self.page = tk.Frame(self.window)
        self.page.pack(side='top')
        

        self.ageLabel = tk.Label(self.page, text='請輸入年齡:')
        self.ageLabel.grid(row=1,column=2)
        self.ageEntry = tk.Entry(self.page)
        self.ageEntry.grid(row=1,column=3,pady=5)

        #點選男女
        self.man_woman=tk.StringVar()
        self.man=tk.Radiobutton(self.page,text='男性',variable=self.man_woman,value='man')
        self.man.grid(row=2,column=2)
        self.man.select()
        self.woman=tk.Radiobutton(self.page,text='女性',variable=self.man_woman,value='woman')
        self.woman.grid(row=2,column=3,pady=5)

        #點選有沒有高血壓
        self.highLabel = tk.Label(self.page, text='是否有高血壓:')
        self.highLabel.grid(row=3,column=2)
        self.high_blood_pressure=tk.StringVar()
        self.bloodyes=tk.Radiobutton(self.page,text='是',variable=self.high_blood_pressure,value='yes')
        self.bloodyes.grid(row=4,column=2)
        self.bloodyes.select()
        self.bloodno=tk.Radiobutton(self.page,text='否',variable=self.high_blood_pressure,value='no')
        self.bloodno.grid(row=4,column=3,pady=5)
        
        #輸入身高
        self.heightLabel = tk.Label(self.page, text='身高(公分):')
        self.heightLabel.grid(row=5,column=2)
        self.height = tk.Entry(self.page)
        self.height.grid(row=5,column=3,pady=5)
        
        #輸入體重
        self.weightLabel = tk.Label(self.page, text='體重(公斤):')
        self.weightLabel.grid(row=6,column=2)
        self.weight = tk.Entry(self.page)
        self.weight.grid(row=6,column=3,pady=5)
        
        #BMI計算
        def cal_BMI():
            weight_value=self.weight.get()
            height_value=self.height.get()

            if weight_value and height_value:
                try:
                    weight_int=int(weight_value)
                    height_int=int(height_value)
                    BMI_value=weight_int/((height_int/100)**2)
                    BMI_value='{:.1f}'.format(BMI_value)
                    self.BMI.set(BMI_value)  # Store BMI value as a class attribute
                    self.BMItext=tk.Label(self.page,text=BMI_value)
                    self.BMItext.grid(row=6,column=3)
                    # print(BMI_value)
                    return BMI_value
                
                except ValueError:
                    print('沒有輸入')
        
        #顯示BMI
        self.BMI=tk.StringVar()
        self.BMILabel=tk.Label(self.page,text='BMI:')
        self.BMILabel.grid(row=7,column=2)
        self.BMIbutton=tk.Button(self.page,text='計算BMI',command=cal_BMI)
        self.BMIbutton.grid(row=6,column=4)
        
        #腰圍
        self.waistlineLabel=tk.Label(self.page,text='頸圍是否超過(男性43cm,女性40cm):')
        self.waistlineLabel.grid(row=8,column=2)
        self.waistline=tk.StringVar()
        self.waistlineyes=tk.Radiobutton(self.page,text='是',variable=self.waistline,value='yes')
        self.waistlineyes.grid(row=9,column=2)
        self.waistlineyes.select()
        self.waistlineno=tk.Radiobutton(self.page,text='否',variable=self.waistline,value='no')
        self.waistlineno.grid(row=9,column=3)
        # self.waistlinetext=tk.Entry(self.page)
        # self.waistlinetext.grid(row=7,column=3)

        #是否有過睡到一辦發現不能呼吸
        self.breathLabel = tk.Label(self.page, text='是否有過睡到一半發現不能呼吸:')
        self.breathLabel.grid(row=10,column=2)
        self.breath=tk.StringVar()
        self.breathyes=tk.Radiobutton(self.page,text='是',variable=self.breath,value='yes')
        self.breathyes.grid(row=11,column=2)
        self.breathyes.select()
        self.breathno=tk.Radiobutton(self.page,text='否',variable=self.breath,value='no')
        self.breathno.grid(row=11,column=3)

        #會不會睡起來還是很累
        self.sleepLabel = tk.Label(self.page, text='會不會睡起來還是很累:')
        self.sleepLabel.grid(row=12,column=2)
        self.sleep=tk.StringVar()
        self.sleepyes=tk.Radiobutton(self.page,text='是',variable=self.sleep,value='yes')
        self.sleepyes.grid(row=13,column=2)
        self.sleepyes.select()
        self.sleepno=tk.Radiobutton(self.page,text='否',variable=self.sleep,value='no')
        self.sleepno.grid(row=13,column=3)

        #跳頁button
        self.button = tk.Button(self.page, text='填寫完畢', command=self.second_page)
        self.button.grid(row=18,column=4)

        
        

    def second_page(self):
        age = int(self.ageEntry.get())
        gender = self.man_woman.get()
        blood_pressure = self.high_blood_pressure.get()
        BMI_value = float(self.BMI.get())  # Retrieve BMI value from class attribute
        waistline_value = self.waistline.get()
        breath_value = self.breath.get()
        tired = self.sleep.get()
        
        risk_level = determine(age, gender, blood_pressure, BMI_value, waistline_value, breath_value, tired)
        
        self.page.destroy()
        SecondPage(self.window, risk_level)

class SecondPage(object):
    def __init__(self, master=None, risk_level=None):
        self.window = master
        self.page = tk.Frame(self.window)
        self.page.pack()

        i=1

        #選頁
        # menu=tk.StringVar()
        # menu.set(('睡眠紀錄','異常數值','建議'))
        # self.listbox=tk.Listbox(self.page,listvariable=menu,height=3)
        # self.listbox.pack(side='right',anchor='ne',padx=5,pady=30)
        # self.listbox.grid(row=22,column=300)

        global right_frame

        right_frame=tk.Frame(self.page)
        right_frame.pack(side='right')

        #日期
        time=datetime.datetime.now().strftime('%Y/%m/%d')
        self.timelabel=tk.Label(right_frame,text='O日期:'+time,anchor='ne',justify='right',font='10').pack(anchor='w')

        #風險等級
        self.risk_label = tk.Label(right_frame, text='O風險等級:'+risk_level,anchor='ne',justify='right',font='10').pack(anchor='w')
        
        #異常數值
        # self.strange=tk.Label(right_frame,text='O異常數值:').pack(anchor='w')

        #正常值
        self.normal=tk.Label(right_frame,text='O正常值').pack(anchor='w')
        #心跳
        self.heartbeat=tk.Label(right_frame,text='心跳:60-100次/分').pack(anchor='w')
        #血氧
        self.spo2_normal=tk.Label(right_frame,text='血氧:95-100%').pack(anchor='w')
        #睡眠呼吸中止症定義
        self.sleep=tk.Label(right_frame,text='O睡眠呼吸中止症定義').pack(anchor='w')
        self.sleep1=tk.Label(right_frame,text='睡眠中每小時內呼吸暫停10秒以上並大於5次').pack(anchor='w')

        #分隔線
        self.divider=tk.Label(right_frame,text='----------------------------------').pack(anchor='w')

        #血氧畫布
        # self.spo2_canvas=tk.Canvas(self.page)
        # self.spo2_canvas.pack()
        #血氧
        # spo2=95 #初始值
        # self.spo2=tk.StringVar()
        # self.spo2.set(spo2)
        # self.spo2Label=tk.Label(right_frame,text='血氧:',font='10').pack(anchor='w')
        # self.spo2textvar=tk.Label(right_frame,textvariable=self.spo2,font='10').pack(anchor='w')

        #開始測量聲音
        self.button_start = tk.Button(self.page,text=u'開始預測聲音',command=self.start_mp)
        self.button_start.pack(side='bottom')

        #開始測量血氧
        # self.button_spo2=tk.Button(self.page,text=u'開始測量血氧',command=self.update_spo2).pack(side='bottom')

        #到輸入主要視窗的按鈕
        self.button_reuslt = tk.Button(self.page, text=u'主頁', command=self.main_page)
        self.button_reuslt.pack(side='bottom')

        #聲音辨識的畫布
        self.audio_canvas=tk.Canvas(self.window)
        self.audio_canvas.pack(side='bottom')

        #openpose
        self.openpose_canvas=tk.Canvas(self.page)
        self.openpose_canvas.pack(side='left')
        app=multiprocessing.Process(target=MyApp(self.openpose_canvas))
        app.start()

    # def update_spo2(self):
        # ser=multiprocessing.Process(target=SerialReaderApp(right_frame))
        # ser.start()
        # data=[]
        # counter=0
        # ser=serial.Serial(com,baudrate,timeout=timeout)
        # ser.flushInput()
        # res=ser.readline().decode()
        # data.append(res)
        # spo2_value=str(res)
        # print('{}'.format(res))
        # counter+=1
        # spo2_value=str(random.randint(90,95))
        # self.spo2.set(spo2_value)
        # self.spo2label=tk.Label(right_frame,text='血氧:',font='10').pack(anchor='w')
        # self.spo2text=tk.Label(right_frame,text=spo2_value,font='10').pack(anchor='w')
        # self.page.after(500,self.update_spo2)

    def start_mp(self):
        animation=multiprocessing.Process(target=create_matplotlib_animation(self.audio_canvas))
        animation.start()

    def main_page(self):
        self.page.destroy()
        FirstPage(self.window)

    
if __name__ == '__main__':
    # Create the main window and run the application
    window = tk.Tk()
    window.title('GUI')
    window.geometry('640x1000')
    window.resizable(False, False)
    
    spo2_window=tk.Tk()
    spo2_window.title('SpO2')
    spo2_window.geometry('200x75')
    spo2_window.resizable(False, False)
    
    #Arduino setting
    # global com, baudrate,timeout
    com='COM4'
    baudrate=9600
    timeout=1

    FirstPage(window)
    # SerialReaderApp(spo2_window)
    # ser=multiprocessing.Process(target=SerialReaderApp(spo2_window))
    # ser.start()
    # SecondPage(window)
    window.mainloop()
