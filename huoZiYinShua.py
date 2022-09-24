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




#--------------------------------------------
#自定义函数
#--------------------------------------------
#文件路径转文件夹路径
def _fileName2FolderName(fileName):
	for i in range(len(fileName)-1, -1, -1):
		if fileName[i] == '\\' or fileName[i] == '/':
			return fileName[0:i+1]



#标准化音频，统一音量
def _normalizeAudio(data):
	rms = np.sqrt(np.mean(data**2))
	normData = data / rms * 0.2
	return normData



#读取音频文件
def _loadAudio(fileDir, norm):
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
	#标准化
	if norm:
		data = _normalizeAudio(data)
	return data



#改变音高和速度
def _modifyPitchAndSpeed(data, pitchMultiple, speedMultiple):
	if (pitchMultiple == 1 and speedMultiple == 1):
		#没有改动的必要，直接返回
		return data
	
	elif (pitchMultiple > 2 or speedMultiple < 0.5):
		print("过于极端的音调和速度参数可能导致输出结果与预期不符，故不作改动")
		return data
	
	else:
		#第一次拉伸
		if (speedMultiple / pitchMultiple == 1):
			#没有拉伸的必要
			step1 = data
		else:
			#不改变音高的同时在时间上拉伸（PSOLA）
			#constant_stretch过小会导致bug，因此分两次拉伸
			step1 = psola.vocode(data, _targetSR, constant_stretch=1/pitchMultiple)
			step1 = psola.vocode(step1, _targetSR, constant_stretch=speedMultiple)
		#第二次拉伸，以改变音高的方式拉伸回来
		newLength = int(len(data) / speedMultiple)
		step2 = np.interp(np.array(range(newLength)), np.linspace(0,newLength-1,len(step1)), step1)
		return step2




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
				pitchMult=1, speedMult=1, norm=False, reverse=False):		
		self.__concatenate(rawData, inYsddMode, pitchMult, speedMult, norm, reverse)
		self.__export(filePath)
		print("已导出到" + filePath + "下")
	
	
	
	#直接播放
	def directPlay(self, rawData, tempPath="./HZYSTempOutput/temp.wav",
					inYsddMode=False, pitchMult=1, speedMult=1, norm=False, reverse=False):
		self.__concatenate(rawData, inYsddMode, pitchMult, speedMult, norm, reverse)
		self.__export(tempPath)
		playsound(tempPath)
	
	
	
	#生成中间文件
	def __concatenate(self, rawData, inYsddMode, pitchMult, speedMult, norm, reverse):
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
																_loadAudio(self.__voicePath
																			+ word + ".wav",
																			norm)))
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
																	+ ".wav",
																	norm)))
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
		self.__concatenated = _modifyPitchAndSpeed(self.__concatenated, pitchMult, speedMult)
		
		#倒放
		if(reverse):
			self.__concatenated = np.flip(self.__concatenated)

		#如果缺失拼音，则发出警告
		if len(missingPinyin) != 0:
			print("警告：缺失或未定义{}".format(missingPinyin))


	
	#导出wav文件
	def __export(self, filePath):
		folderPath = _fileName2FolderName(filePath)
		if not Path(folderPath).exists():
			Path(folderPath).mkdir()
		sf.write(filePath, self.__concatenated, _targetSR)
