import json
import ctypes
from tkinter import Tk, Button, messagebox, scrolledtext
from huoZiYinShua import *

#打开设置文件
configFile= open(".\\settings.json", encoding="utf8")
settings = json.load(configFile)
configFile.close()

#读取设置
outputFile = settings["outputFile"]		#输出文件 (wav)

#新建活字印刷类实例
HZYS = huoZiYinShua(settings)


#主框架
topFrame = Tk()
#设置窗口大小
topFrame.geometry("480x320")
#获取缩放因子
ctypes.windll.shcore.SetProcessDpiAwareness(1)
ScaleFactor=ctypes.windll.shcore.GetScaleFactorForDevice(0)
#设置缩放因子
topFrame.tk.call('tk', 'scaling', ScaleFactor/75)
#窗口标题
topFrame.title("欧炫！纯纯的活字印刷")

#文本框
textArea = scrolledtext.ScrolledText(topFrame, width=50, height=15)

#直接播放的监听事件
def onDirectPlay():
    textToRead = textArea.get(1.0, 'end')
    HZYS.directPlay(textToRead)

#导出的监听事件
def onExport():
    textToRead = textArea.get(1.0, 'end')
    HZYS.export(textToRead, outputFile)
    messagebox.showinfo("疑似是成功了", "已导出到当前目录Output.wav下")
    pass

#按钮们
playButton = Button(topFrame, text="直接播放", command=onDirectPlay, height=1, width=8)
playButton.place(x=100, y=260)
exportButton = Button(topFrame, text="导出", command=onExport, height=1, width=8)
exportButton.place(x=280, y=260)

#控件打包
textArea.pack()
topFrame.mainloop()