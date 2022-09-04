from platform import system
from tkinter import Checkbutton, Tk, Button, messagebox, scrolledtext, filedialog
from tkinter import BooleanVar, font
from huoZiYinShua import *
from multiprocessing import Process, freeze_support
from PIL import ImageTk, Image


#新建活字印刷类实例
HZYS = huoZiYinShua("./settings.json")
#播放音频的进程
myProcess = Process()



#主框架
#-------------------------------------------
topFrame = Tk()



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
textArea = scrolledtext.ScrolledText(topFrame, width=50, height=11,
									font=font.Font(family="微软雅黑", size=10))


#复选框
ysddCkBt = Checkbutton(topFrame, text="匹配到特定文字时使用原声大碟",
						variable=inYsddMode, onvalue=True, offvalue=False,
						font=font.Font(family="微软雅黑", size=10))


#按钮们
#播放按钮
playButton = Button(topFrame, text="直接播放", command=onDirectPlay, height=1, width=8,
					font=font.Font(family="微软雅黑", size=11))


#导出按钮
exportButton = Button(topFrame, text="导出", command=onExport, height=1, width=8,
					font=font.Font(family="微软雅黑", size=11))



#主函数
#-------------------------------------------
if __name__ == "__main__":
	#multiprocess和Windows的兼容
	freeze_support()
	#匹配DPI
	if (system() == "Windows"):
		from ctypes import windll
		windll.shcore.SetProcessDpiAwareness(1)

	#主窗口
	#-----------------------------
	#设置窗口大小
	topFrame.geometry("480x320")
	#窗口图标
	try:
		img = ImageTk.PhotoImage(Image.open("./lizi.ico"))
		topFrame.tk.call('wm', 'iconphoto', topFrame._w, img)
	except:
		messagebox.showinfo("警告", "缺失图标")
	#窗口标题
	topFrame.title("欧炫！纯纯的活字印刷")

	#元素属性
	#-----------------------------
	textArea.place(x=0, y=0)
	ysddCkBt.place(x=20, y=230)
	playButton.place(x=100, y=265)
	exportButton.place(x=280, y=265)


	#控件打包
	textArea.pack()
	topFrame.mainloop()

	#退出
	try:
		myProcess.terminate()
	except:
		pass