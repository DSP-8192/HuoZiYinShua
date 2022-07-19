from huoZiYinShua import *
import json
import os


if __name__ == "__main__":
	#打开设置文件
	configFile= open(".\\settings.json", encoding="utf8")
	settings = json.load(configFile)
	configFile.close()
	
	#读取设置
	sourceDir = settings["sourceDirectory"]		#音频文件存放目录
	dictDir = settings["dictDirectory"]			#词典存放目录
	inputDir = settings["inputDirectory"]		#输入目录
	outputDir = settings["outputDirectory"]		#输出目录

	#读取要活字印刷的内容
	textFile = open(inputDir, encoding="utf8")
	textToRead = textFile.read()
	textFile.close()
	
	#新建活字印刷类实例
	HZYS = huoZiYinShua(sourceDir, dictDir)
	#导出
	HZYS.export(textToRead, outputDir)
	os.system("pause")
