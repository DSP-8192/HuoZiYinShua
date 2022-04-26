from huoZiYinShua import *



if __name__ == "__main__":
	f1 = open(".//test1.txt", "r", encoding = "utf-8")
	f2 = open(".//test2.txt", "r", encoding = "utf-8")
	text1 = f1.read()
	text2 = f2.read()
	f1.close()
	f2.close()


	HZYS = huoZiYinShua(".//素材//", ".//dictionary.csv")
	HZYS.execute(text1)
	HZYS.export("output1.wav")
	HZYS.execute(text2)
	HZYS.export("output2.wav")
	
