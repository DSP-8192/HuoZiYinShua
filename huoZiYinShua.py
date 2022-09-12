# -*- coding: UTF-8 -*-
#鬼畜音源的活字印刷
#作者：DSP_8192

from librosa import load as librosa_load
from librosa.effects import pitch_shift
from soundfile import write as sf_write
from playsound import playsound

from numpy import array as np_array
from pypinyin import lazy_pinyin
import json
from pathlib import Path



_keyWordPitchMap = {
	"laotou": -5,
	"xiaohai": 12,
	"xingzhuan": 6
}



#文件路径转文件夹路径
def _fileName2FolderName(fileName):
	for i in range(len(fileName)-1, -1, -1):
		if fileName[i] == '\\' or fileName[i] == '/':
			return fileName[0:i+1]



#活字印刷类
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
		print("已导出到当前目录" + filePath + "下")
	
	
	
	#直接播放
	def directPlay(self, rawData, tempPath="./HZYSTempOutput/temp.wav",
					inYsddMode=False, pitchShift="xingzhuan"):
		self.__concatenate(rawData, inYsddMode, pitchShift)
		self.__export(tempPath)
		playsound(tempPath)
	
	
	
	#生成中间文件
	def __concatenate(self, rawData, inYsddMode, pitchShift):
		missingPinyin = []
		self.__concatenated = []
		
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
							self.__concatenated += librosa_load(path=self.__voicePath + word + ".wav",
																sr=44100, mono=True)[0].tolist()
						except:
							if word not in missingPinyin:
								missingPinyin.append(word)
							self.__concatenated += list(0 for i in range(0, 10000))
			#使用原声大碟
			else:
				try:
					self.__concatenated += librosa_load(path=self.__ysddPath + self.__ysddTable[pronunciations[i][0]] + ".wav",
														sr=44100, mono=True)[0].tolist()
				except:
					if self.__ysddTable[pronunciations[i][0]] not in missingPinyin:
						missingPinyin.append(self.__ysddTable[pronunciations[i][0]])
					self.__concatenated += list(0 for i in range(0, 10000))


		#音高偏移
		if (pitchShift != "disabled"):
			self.__concatenated = np_array(self.__concatenated)
			self.__concatenated = pitch_shift(y=self.__concatenated, sr=44100,
											n_steps=_keyWordPitchMap[pitchShift])
			self.__concatenated = self.__concatenated.tolist()
		

		#如果缺失拼音，则发出警告
		if len(missingPinyin) != 0:
			print("警告：缺失或未定义{}".format(missingPinyin))
		

	
	#导出wav文件
	def __export(self, filePath):
		folderPath = _fileName2FolderName(filePath)
		if not Path(folderPath).exists():
			Path(folderPath).mkdir()
		sf_write(file=filePath, data=np_array(self.__concatenated), samplerate=44100)
