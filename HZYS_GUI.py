import os
import sys
import json
from tkinter import *
from tkinter import scrolledtext
from tkinter import messagebox
from huoZiYinShua import *

#打开设置文件
configFile= open(".\\settings.json", encoding="utf8")
settings = json.load(configFile)
configFile.close()

#读取设置
sourceDir = settings["sourceDirectory"]		#音频文件存放目录
dictFile = settings["dictFile"]			#词典存放文件 (csv)
outputFile = settings["outputFile"]		#输出文件 (wav)

#新建活字印刷类实例
HZYS = huoZiYinShua(sourceDir, dictFile)


#主框架
topFrame = Tk()
#设置窗口大小
topFrame.geometry("480x320")
#窗口标题
topFrame.title("欧炫！纯纯的活字印刷")

#文本框
textArea = scrolledtext.ScrolledText(topFrame, width=40, height=10)

#直接播放的监听事件
def onDirectPlay():
    textToRead = textArea.get(1.0, 'end')
    # 由于某些原因，这里使用winsound
    # playsound有文件占用问题，无法在程序运行中对临时文件进行改动
    HZYS.export(textToRead, '.\HZYSTempOutput\\temp.wav')
    import winsound
    winsound.PlaySound('.\HZYSTempOutput\\temp.wav', winsound.SND_FILENAME|winsound.SND_ASYNC)
    pass

#导出的监听事件
def onExport():
    textToRead = textArea.get(1.0, 'end')
    HZYS.export(textToRead, outputFile)
    messagebox.showinfo("疑似是成功了", "已导出到当前目录Output.wav下")
    pass

#按钮们
playButton = Button(topFrame, text="直接播放", command=onDirectPlay)
exportButton = Button(topFrame, text="导出", command=onExport)

#控件打包
textArea.pack()
playButton.pack()
exportButton.pack()
topFrame.mainloop()