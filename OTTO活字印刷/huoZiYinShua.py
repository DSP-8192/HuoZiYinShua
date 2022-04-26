# -*- coding: UTF-8 -*-
from pydub import AudioSegment
from pypinyin import lazy_pinyin
import csv



class huoZiYinShua:	
	def __init__(self, voicePath, dictionaryPath):
		self.voicePath = voicePath
		self.dictionary = list(csv.reader(open(dictionaryPath)))
		self.dictionary = list(zip(*(self.dictionary)))
		
	
	#生成
	def execute(self, rawData):
		missingPinyin = []
		self.concatenated = AudioSegment.empty()
		
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
					self.concatenated += AudioSegment.from_file(self.voicePath + word + ".wav", format = "wav")
					self.concatenated += AudioSegment.silent(duration = 100)
				except:
					if word not in missingPinyin:
						missingPinyin.append(word)
					self.concatenated += AudioSegment.silent(duration = 350)
		
		#如果缺失拼音，则发出警告
		if len(missingPinyin) != 0:
			print("警告：缺失以下内容：")
			print(missingPinyin)
		


	def export(self, fileName):
		self.concatenated.export(fileName, format = "wav")
		print("已导出" + fileName)



if __name__ == "__main__":
	print("sdfg")
