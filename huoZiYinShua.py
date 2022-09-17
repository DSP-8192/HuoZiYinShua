# -*- coding: UTF-8 -*-
#鬼畜音源的活字印刷
#作者：DSP_8192

import soundfile as sf
import psola
import numpy as np
from playsound import playsound
from pypinyin import lazy_pinyin
import json
from pathlib import Path




#--------------------------------------------
#全局变量
#--------------------------------------------
#目标采样率
_targetSR = 44100

#关键词与频率伸缩系数对照
_keyWordPitchMap = {
	"laotou": 0.8,
	"xiaohai": 1.5,
	"xingzhuan": 1.3
}




#--------------------------------------------
#自定义函数
#--------------------------------------------
#文件路径转文件夹路径
def _fileName2FolderName(fileName):
	for i in range(len(fileName)-1, -1, -1):
		if fileName[i] == '\\' or fileName[i] == '/':
			return fileName[0:i+1]



#读取音频文件
def _loadAudio(fileDir):
	data, sampleRate = sf.read(fileDir)
	#双声道转单声道
	if (len(data.shape) == 2):
		#左右声道相加除以2
		data = (data[:, 0] + data[:, 1]) / 2
	
	#统一采样率
	if (sampleRate != _targetSR):
		#计算转换后的长度
		newLength = int((_targetSR / sampleRate) * len(data))
		#转换
		data = np.interp(np.array(range(newLength)), np.linspace(0,newLength-1,len(data)), data)
	
	return data



#移动音高
def _shiftPitch(data, scaleFactor):
	#不改变音高的同时在时间上拉伸（PSOLA）
	dataStretched = psola.vocode(data, _targetSR, constant_stretch=1/scaleFactor)
	#拉伸至原来的长度，但是改变原来的音高
	dataPitchShifted = np.interp(np.array(range(len(data))),
								np.linspace(0,len(data)-1,len(dataStretched)), dataStretched)
	return dataPitchShifted




#--------------------------------------------
#活字印刷类
#--------------------------------------------
class huoZiYinShua:
	def __init__(self, configFileLoc):
		try:
			self.config(configFileLoc)
			self.__configSucceed = True
		except Exception as e:
			self.__configSucceed = False
			print(e)		



	#配置是否成功
	def configSucceed(self):
		return self.__configSucceed



	#配置
	def config(self, configFileLoc):
		#读取设置文件
		configFile = open(configFileLoc, encoding="utf8")
		configuration = json.load(configFile)
		configFile.close()

		dictFile = open(configuration["dictFile"], encoding="utf8")					#读取单字词典 (json)
		ysddTableFile = open(configuration["ysddTableFile"], encoding="utf8")		#读取原声大碟文本与文件名对照表 (json)

		self.__voicePath = configuration["sourceDirectory"]					#单字音频文件存放目录
		self.__ysddPath = configuration["ysddSourceDirectory"]				#原声大碟音频文件存放目录
		self.__dictionary = json.load(dictFile)								#定义非中文字符读法的词典
		self.__ysddTable = json.load(ysddTableFile)							#原声大碟文本与文件名对照表

		self.__ysddTable = sorted(self.__ysddTable.items(), key=lambda x:len(x[0]), reverse=True)	#从长到短排序
		self.__ysddTable = dict(self.__ysddTable)


	
	#直接导出
	def export(self, rawData, filePath="./Output.wav", inYsddMode=False,
				pitchShift="disabled"):		
		self.__concatenate(rawData, inYsddMode, pitchShift)
		self.__export(filePath)
		print("已导出到" + filePath + "下")
	
	
	
	#直接播放
	def directPlay(self, rawData, tempPath="./HZYSTempOutput/temp.wav",
					inYsddMode=False, pitchShift="disabled"):
		self.__concatenate(rawData, inYsddMode, pitchShift)
		self.__export(tempPath)
		playsound(tempPath)
	
	
	
	#生成中间文件
	def __concatenate(self, rawData, inYsddMode, pitchShift):
		missingPinyin = []
		self.__concatenated = np.array([])
		
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
							self.__concatenated = np.concatenate((self.__concatenated,
																_loadAudio(self.__voicePath + word + ".wav")))
						#如果出现错误
						except Exception as e:
							print(e)		#显示错误信息
							#加入缺失素材列表
							if word not in missingPinyin:
								missingPinyin.append(word)
							#以空白音频代替
							self.__concatenated = np.concatenate((self.__concatenated,
																np.zeros(int(_targetSR/4))))
			
			#使用原声大碟
			else:
				#拼接
				try:
					self.__concatenated = np.concatenate((self.__concatenated,
														_loadAudio(self.__ysddPath
																	+ self.__ysddTable[pronunciations[i][0]]
																	+ ".wav")))
				#如果出现错误
				except Exception as e:
					print(e)		#显示错误信息
					#加入缺失素材列表
					if self.__ysddTable[pronunciations[i][0]] not in missingPinyin:
						missingPinyin.append(self.__ysddTable[pronunciations[i][0]])
					#以空白音频代替
					self.__concatenated = np.concatenate((self.__concatenated,
														np.zeros(int(_targetSR/4))))


		#音高偏移
		if (pitchShift != "disabled"):
			self.__concatenated = _shiftPitch(self.__concatenated,
											_keyWordPitchMap[pitchShift])
		

		#如果缺失拼音，则发出警告
		if len(missingPinyin) != 0:
			print("警告：缺失或未定义{}".format(missingPinyin))
		

	
	#导出wav文件
	def __export(self, filePath):
		folderPath = _fileName2FolderName(filePath)
		if not Path(folderPath).exists():
			Path(folderPath).mkdir()
		sf.write(filePath, self.__concatenated, _targetSR)
