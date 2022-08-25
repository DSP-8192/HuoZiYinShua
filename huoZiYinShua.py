# -*- coding: UTF-8 -*-
#鬼畜音源的活字印刷
#作者：DSP_8192

from pydub import AudioSegment
from pypinyin import lazy_pinyin
import csv
import json
from pathlib import Path
import playsound


#文件路径转文件夹路径
def _fileName2FolderName(fileName):
	for i in range(len(fileName)-1, -1, -1):
		if fileName[i] == '\\' or fileName[i] == '/':
			return fileName[0:i+1]



class huoZiYinShua:
	def __init__(self, configFileLoc):
		#读取设置文件
		configFile = open(configFileLoc, encoding="utf8")
		configuration = json.load(configFile)
		configFile.close()

		dictFile = open(configuration["dictFile"], encoding="utf8")			#读取单字词典 (csv)
		ysddTableFile = open(configuration["ysddTableFile"], encoding="utf8")		#读取原声大碟文本与文件名对照表 (csv)

		self.__voicePath = configuration["sourceDirectory"]					#单字音频文件存放目录
		self.__ysddPath = configuration["ysddSourceDirectory"]				#原声大碟音频文件存放目录
		self.__dictionary = dict(csv.reader(dictFile, delimiter=","))		#词典存放文件 (csv)
		self.__ysddTable = dict(csv.reader(ysddTableFile, delimiter="\t"))	#原声大碟文本与文件名对照表 (csv)

		self.__ysddTable = sorted(self.__ysddTable.items(), key=lambda x:len(x[0]), reverse=True)	#从长到短排序
		self.__ysddTable = dict(self.__ysddTable)


	
	#直接导出
	def export(self, rawData, filePath=".\\Output.wav", inYsddMode=False):		
		self.__concatenate(rawData, inYsddMode)
		self.__export(filePath)
		print("已导出到当前目录" + filePath + "下")
	
	
	
	#直接播放
	def directPlay(self, rawData, tempPath=".\\HZYSTempOutput\\temp.wav", inYsddMode=False):
		self.__concatenate(rawData, inYsddMode)
		self.__export(tempPath)
		playsound.playsound(tempPath)
	
	
	
	#生成中间文件
	def __concatenate(self, rawData, inYsddMode):
		missingPinyin = []
		self.__concatenated = AudioSegment.empty()
		
		#预处理，转为小写
		rawData = rawData.lower()
		pronunciations = []

		#分割使用活字印刷的部分和使用原声大碟的部分
		splitted = [[rawData, False]]		#[文本, 是否使用原声大碟]
		#遍历要匹配的句子
		if inYsddMode:
			for ysdd in self.__ysddTable.items():
				#遍历文本
				i = -1
				while i < (len(splitted) - 1):
					i += 1
					if splitted[i][1]:		#已经被划分为原声大碟部分
						continue
					#存在匹配
					if ysdd[0] in splitted[i][0]:
						indexBegin = splitted[i][0].index(ysdd[0])		#获取开始位置
						#分割
						splitted.insert(i+1, [splitted[i][0][indexBegin:indexBegin+len(ysdd[0])], True])
						splitted.insert(i+2, [splitted[i][0][indexBegin+len(ysdd[0]):], False])
						splitted[i][0] = splitted[i][0][0:indexBegin]
					

		#转换自定义的字符
		for i in range(0, len(splitted)):
			pronunciations.append([])
			#使用活字印刷
			if (not splitted[i][1]):
				pronunciations[i].append("")
				for ch in splitted[i][0]:
					if ch in self.__dictionary:
						#词典中存在匹配，转换
						pronunciations[i][0] += self.__dictionary[ch] + " "
					else:
						#保持不变
						pronunciations[i][0] += ch + " "
				pronunciations[i].append(False)		#标记
			#使用原声大碟
			else:
				pronunciations[i].append(splitted[i][0])	#直接复制
				pronunciations[i].append(True)		#标记

		
		#拼接音频
		for i in range(0, len(pronunciations)):
			#使用活字印刷
			if (not pronunciations[i][1]):
				#将汉字转换成拼音
				pinyin = lazy_pinyin(pronunciations[i][0])
				#拆成单独的字
				for text in pinyin:
					for word in text.split():
						#拼接每一个字
						try:
							self.__concatenated += AudioSegment.from_file(self.__voicePath + word + ".wav", format = "wav")
						except:
							if word not in missingPinyin:
								missingPinyin.append(word)
							self.__concatenated += AudioSegment.silent(duration = 250)
			#使用原声大碟
			else:
				try:
					self.__concatenated += AudioSegment.from_file(self.__ysddPath + self.__ysddTable[pronunciations[i][0]] + ".wav", format = "wav")
				except:
					if self.__ysddTable[pronunciations[i][0]] not in missingPinyin:
						missingPinyin.append(self.__ysddTable[pronunciations[i][0]])
					self.__concatenated += AudioSegment.silent(duration = 250)

		#如果缺失拼音，则发出警告
		if len(missingPinyin) != 0:
			print("警告：缺失或未定义{}".format(missingPinyin))
		

	
	#导出wav文件
	def __export(self, filePath):
		folderPath = _fileName2FolderName(filePath)
		if not Path(folderPath).exists():
			Path(folderPath).mkdir()
		self.__concatenated.export(filePath, format = "wav")
