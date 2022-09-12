from platform import system
from tkinter import Tk, Toplevel
from tkinter import messagebox, filedialog
from tkinter import Checkbutton, Button, scrolledtext, OptionMenu
from tkinter import Label, font, BooleanVar, StringVar
from huoZiYinShua import *
from multiprocessing import Process, freeze_support
from PIL import ImageTk, Image
import json


#新建活字印刷类实例
HZYS = huoZiYinShua("./settings.json")
#播放音频的进程
myProcess = Process()



#主框架
#-------------------------------------------
mainWindow = Tk()



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
						kwargs={"rawData": textToRead, "inYsddMode": inYsddMode.get(),
								"pitchShift": optionConvertMap[pitchShiftOption.get()]})
	myProcess.start()


#导出的监听事件
def onExport():
	textToRead = textArea.get(1.0, 'end')
	outputFile = filedialog.asksaveasfilename(title="选择导出路径",
											filetypes = (("wav音频文件", "*.wav"),))
	if(outputFile != ""):
		if not outputFile.endswith(".wav"):
			outputFile += ".wav"
		HZYS.export(textToRead, filePath=outputFile, inYsddMode=inYsddMode.get(),
					pitchShift=optionConvertMap[pitchShiftOption.get()])
		messagebox.showinfo("疑似是成功了", "已导出到" + outputFile +"下")


#读取设定文件
def readConfig():
	#若./settings.json存在
	try:
		configFile = open("./settings.json", "r", encoding="utf8")
		configuration = json.load(configFile)
		configFile.close()
		return configuration
	#若不存在
	except:
		configuration = {
			"sourceDirectory": "",
			"ysddSourceDirectory": "",
			"dictFile": "",
			"ysddTableFile": ""
		}
		return configuration


#更改设定
def setConfig(option, texts):
	#读取当前设定
	configuration = readConfig()
	userConfig = ""
	#让用户选择文件或目录
	if (option == "sourceDirectory" or option == "ysddSourceDirectory"):
		userConfig = filedialog.askdirectory(title="选择文件夹") + "/"
	elif (option == "dictFile" or option == "ysddTableFile"):
		userConfig = filedialog.askopenfilename(title="选择文件",
											filetypes = (("json配置文件", "*.json"),))
	#写入
	configuration[option] = userConfig
	configFile = open("./settings.json", "w", encoding="utf8")
	json.dump(configuration, configFile, ensure_ascii=False, indent="\t")
	configFile.close()
	#更新配置窗口
	optionArray = ["sourceDirectory", "ysddSourceDirectory", "dictFile", "ysddTableFile"]
	texts[optionArray.index(option)].configure(text=configuration[option])
	#更新活字印刷实例配置
	HZYS.config("./settings.json")



#创建设定窗口
def createConfigWindow():
	#窗口属性
	configWindow = Toplevel(mainWindow)
	configWindow.geometry("480x400")
	configWindow.title("设定")
	try:
		img = ImageTk.PhotoImage(Image.open("./lizi.ico"))
		configWindow.tk.call('wm', 'iconphoto', configWindow._w, img)
	except:
		messagebox.showwarning("警告", "缺失图标")
	#读取设置
	configuration = readConfig()

	#文字
	text1_1 = Label(configWindow, text="活字印刷单字音频存放文件夹：",
					font=font.Font(family="微软雅黑", size=11))
	text1_2 = Label(configWindow, text=configuration["sourceDirectory"])
	text2_1 = Label(configWindow, text="活字印刷原声大碟音频存放文件夹：",
					font=font.Font(family="微软雅黑", size=11))
	text2_2 = Label(configWindow, text=configuration["ysddSourceDirectory"])
	text3_1 = Label(configWindow, text="非中文字符读法字典文件：",
					font=font.Font(family="微软雅黑", size=11))
	text3_2 = Label(configWindow, text=configuration["dictFile"])
	text4_1 = Label(configWindow, text="原声大碟关键词与音频对照表：",
					font=font.Font(family="微软雅黑", size=11))
	text4_2 = Label(configWindow, text=configuration["ysddTableFile"])
	texts = [text1_2, text2_2, text3_2, text4_2]

	#按钮
	configButton1 = Button(configWindow, text="选择目录", command=lambda: setConfig("sourceDirectory", texts),
					height=1, width=8, font=font.Font(family="微软雅黑", size=11))
	configButton2 = Button(configWindow, text="选择目录", command=lambda: setConfig("ysddSourceDirectory", texts),
					height=1, width=8, font=font.Font(family="微软雅黑", size=11))
	configButton3 = Button(configWindow, text="选择文件", command=lambda: setConfig("dictFile", texts),
					height=1, width=8, font=font.Font(family="微软雅黑", size=11))
	configButton4 = Button(configWindow, text="选择文件", command=lambda: setConfig("ysddTableFile", texts),
					height=1, width=8, font=font.Font(family="微软雅黑", size=11))

	#位置
	text1_1.place(x=0, y=0)
	text1_2.place(x=0, y=20)
	text2_1.place(x=0, y=100)
	text2_2.place(x=0, y=120)
	text3_1.place(x=0, y=200)
	text3_2.place(x=0, y=220)
	text4_1.place(x=0, y=300)
	text4_2.place(x=0, y=320)
	configButton1.place(x=0, y=40)
	configButton2.place(x=0, y=140)
	configButton3.place(x=0, y=240)
	configButton4.place(x=0, y=340)
	


#储存生成选项的变量
#-------------------------------------------
inYsddMode = BooleanVar()
pitchShiftOption = StringVar()
optionConvertMap = {
	"正常": "disabled",
	"说的道莉": "xingzhuan",
	"说的老理": "laotou",
	"谁家小孩": "xiaohai"
}



#GUI元素
#-------------------------------------------
#文本框
textArea = scrolledtext.ScrolledText(mainWindow, width=55, height=11,
									font=font.Font(family="微软雅黑", size=10))


#复选框
ysddCkBt = Checkbutton(mainWindow, text="匹配到特定文字时使用原声大碟",
						variable=inYsddMode, onvalue=True, offvalue=False,
						font=font.Font(family="微软雅黑", size=10))


#按钮们
#播放按钮
playButton = Button(mainWindow, text="直接播放", command=onDirectPlay, height=1, width=8,
					font=font.Font(family="微软雅黑", size=11))


#导出按钮
exportButton = Button(mainWindow, text="导出", command=onExport, height=1, width=8,
					font=font.Font(family="微软雅黑", size=11))


#设置按钮
configButton = Button(mainWindow, text="设置", command=createConfigWindow, height=1, width=8,
					font=font.Font(family="微软雅黑", size=11))


#音调偏移文本
pitchShiftLabel = Label(mainWindow, text="音调偏移选项：",
					font=font.Font(family="微软雅黑", size=10))


#音调偏移
pitchShiftMenu = OptionMenu(mainWindow, pitchShiftOption,
							*list(optionConvertMap.keys()))





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
	mainWindow.geometry("480x360")
	#窗口图标
	try:
		img = ImageTk.PhotoImage(Image.open("./lizi.ico"))
		mainWindow.tk.call('wm', 'iconphoto', mainWindow._w, img)
	except:
		messagebox.showwarning("警告", "缺失图标")
	#窗口标题
	mainWindow.title("欧炫！纯纯的活字印刷")

	#元素属性
	#-----------------------------
	textArea.place(x=10, y=0)

	playButton.place(x=70, y=230)
	exportButton.place(x=190, y=230)
	configButton.place(x=310, y=230)

	ysddCkBt.place(x=20, y=280)
	pitchShiftLabel.place(x=20, y=310)
	pitchShiftOption.set("正常")
	pitchShiftMenu.place(x=110, y=310)


	#检查活字印刷实例是否配置正确
	if not HZYS.configSucceed():
		messagebox.showerror("配置活字印刷实例失败", "请检查设置的文件路径是否正确")
	
	#启动主窗口
	mainWindow.mainloop()

	#退出
	try:
		myProcess.terminate()
	except:
		pass