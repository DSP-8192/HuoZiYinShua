from huoZiYinShua import *
import json
import sys
import os
import argparse

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="使用程序进行电棍活版印刷")
	parser.add_argument('-t', '--text', help="要输出的文字", default="null")
	parser.add_argument("-d", '--directplay', help="直接播放声音", default=False, action="store_true")
	parser.add_argument('-o', '--output', help="输出音频文件名称，例如:./输出.wav", default=".\\Output.wav")
	parser.add_argument('-f', '--file', help="读取的文件名称", default="textToRead.txt")
	#打开设置文件
	configFile = open(".\\settings.json", encoding="utf8")
	settings = json.load(configFile)
	configFile.close()
	
	#读取设置
	inputFile = settings["inputFile"]		#输入文件 (txt)
	outputFile = settings["outputFile"]		#输出文件 (wav)

	#新建活字印刷类实例
	HZYS = huoZiYinShua(settings)
	#要印刷的文本
	textToRead = "我是你跌"

	args = parser.parse_args()
	#判定是否启用命令行模式
	if (len(sys.argv) > 1):
		if (args.text == "null"):
			#设定文件目录并输出文件
			inputFile = args.file
			#读取要活字印刷的内容
			textFile = open(inputFile, encoding="utf8")
			textToRead = textFile.read()
			textFile.close()
			pass
		else:
			#使用文本，不读取文件
			textToRead = args.text
			pass
		#人性化处理，手动加入相对文件路径
		outputFile = args.output
		if (outputFile.startswith("./") or outputFile.startswith(".\\")):
			#用户知情达理
			pass
		else:
			#一般用户
			outputFile = './' + outputFile
		pass
	else:
		#读取要活字印刷的内容
		textFile = open(inputFile, encoding="utf8")
		textToRead = textFile.read()
		textFile.close()
	
	print("输出文本:" + textToRead)
	#判定命令行参数，确定是否直接播放声音
	#(不会对直接运行造成影响)
	if (args.directplay == True):
		print('直接播放')
		HZYS.directPlay(textToRead)
	else:
		#导出
		HZYS.export(textToRead, outputFile)
	os.system("pause")
