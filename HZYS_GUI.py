import ctypes
from tkinter import Checkbutton, Tk, Button, messagebox, scrolledtext, filedialog, BooleanVar
import os
from huoZiYinShua import *
from multiprocessing import Process, freeze_support


#新建活字印刷类实例
HZYS = huoZiYinShua(".\\settings.json")
#播放音频的进程
myProcess = Process()



#主框架
#-------------------------------------------
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



#动作
#-------------------------------------------
#直接播放的监听事件
def onDirectPlay():
	global myProcess
	#停止播放按钮上次点击时播放的音频
	try:
		myProcess.terminate()
	except:
		pass
	#播放
	textToRead = textArea.get(1.0, 'end')
	myProcess = Process(target=HZYS.directPlay,
						kwargs={"rawData": textToRead, "inYsddMode": inYsddMode.get()})
	myProcess.start()


#导出的监听事件
def onExport():
	textToRead = textArea.get(1.0, 'end')
	outputFile = filedialog.asksaveasfilename(title="选择导出路径",
											filetypes = (("wav音频文件", "*.wav*"),))
	if(outputFile != ""):
		if not outputFile.endswith(".wav"):
			outputFile += ".wav"
		HZYS.export(textToRead, filePath=outputFile, inYsddMode=inYsddMode.get())
		messagebox.showinfo("疑似是成功了", "已导出到" + outputFile +"下")



#生成选项
#-------------------------------------------
inYsddMode = BooleanVar()



#GUI元素
#-------------------------------------------
#文本框
textArea = scrolledtext.ScrolledText(topFrame, width=50, height=13)
textArea.place(x=0, y=0)


#复选框
ysddCkBt = Checkbutton(topFrame, text="匹配到特定文字时使用原声大碟",
						variable=inYsddMode, onvalue=True, offvalue=False)
ysddCkBt.place(x=20, y=220)


#按钮们
#播放按钮
playButton = Button(topFrame, text="直接播放", command=onDirectPlay, height=1, width=8)
playButton.place(x=100, y=260)

#导出按钮
exportButton = Button(topFrame, text="导出", command=onExport, height=1, width=8)
exportButton.place(x=280, y=260)



#主函数
#-------------------------------------------
if __name__ == "__main__":
	freeze_support()

	#控件打包
	textArea.pack()
	topFrame.mainloop()

	#退出
	try:
		myProcess.terminate()
	except:
		pass
	os._exit(0)