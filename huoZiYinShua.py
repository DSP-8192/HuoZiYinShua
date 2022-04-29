# -*- coding: UTF-8 -*-
#鬼畜音源的活字印刷
#作者：DSP_8192

from pydub import AudioSegment
from pypinyin import lazy_pinyin
from playsound import playsound
import csv
from pathlib import Path



class huoZiYinShua:	
	def __init__(self, voicePath, dictionaryPath):
		self.voicePath = voicePath
		self.dictionary = list(csv.reader(open(dictionaryPath)))
		self.dictionary = list(zip(*(self.dictionary)))
		
	
	
	#直接导出
	def export(self, rawData, filePath):		
		self.__execute(rawData)
		self.__export(filePath)
		print("已导出" + filePath)
	
	
	
	#直接播放
	def playtext(self, rawData, tempPath = ".\\HZYSTempOutput\\temp.wav"):
		self.__execute(rawData)
		self.__export(tempPath)
		playsound(tempPath)
	
	
	
	#生成中间文件
	def __execute(self, rawData):
		missingPinyin = []
		self.__concatenated = AudioSegment.empty()
		
		#预处理，转为小写
		rawData = rawData.lower()
		sentence = ""
		#处理每一个符号
		for ch in rawData:
			if ch in self.dictionary[0]:
				#词典中存在匹配，转换
				sentence += self.dictionary[1][self.dictionary[0].index(ch)] + " "
			else:
				#保持不变
				sentence += ch + " ";
				
		
		#将汉字转换成拼音
		pinyinTexts = lazy_pinyin(sentence)
		#拆成单独的字
		for text in pinyinTexts:
			for word in text.split():
				#拼接每一个字
				try:
					self.__concatenated += AudioSegment.from_file(self.voicePath + word + ".wav", format = "wav")
					self.__concatenated += AudioSegment.silent(duration = 100)
				except:
					if word not in missingPinyin:
						missingPinyin.append(word)
					self.__concatenated += AudioSegment.silent(duration = 350)
		
		#如果缺失拼音，则发出警告
		if len(missingPinyin) != 0:
			print("警告：缺失以下内容：")
			print(missingPinyin)
		

	
	#导出wav文件
	def __export(self, filePath):
		folderPath = self.__fileName2FolderName(filePath)
		if not Path(folderPath).exists():
			Path(folderPath).mkdir()
		self.__concatenated.export(filePath, format = "wav")
	
	
	
	#文件路径转文件夹路径
	def __fileName2FolderName(self, fileName):
		for i in range(len(fileName)-1, -1, -1):
			if fileName[i] == '\\' or fileName[i] == '/':
				return fileName[0:i+1]
