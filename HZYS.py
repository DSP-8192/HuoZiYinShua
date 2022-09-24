from huoZiYinShua import *
import argparse

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="使用程序进行电棍活版印刷")
	parser.add_argument("-t", "--text", help="要输出的文字", default="我是你跌")
	parser.add_argument("-d", "--directplay", help="直接播放声音", default=False, action="store_true")
	parser.add_argument("-o", "--output", help="输出音频文件名称，例如./输出.wav", default="./Output.wav")
	parser.add_argument("-f", "--file", help="读取的文件名称，例如./输入.txt", default="")
	parser.add_argument("-y", "--inYsddMode", help="匹配到特定文字时使用原声大碟", default=False, action="store_true")
	parser.add_argument("-p", "--pitchMult", help="音调偏移程度，大于1升高音调，小于1降低音调，建议[0.5, 2]", default=1)
	parser.add_argument("-s", "--speedMult", help="播放速度，大于1加速，小于1减速，建议[0.5, 2]", default=1)
	parser.add_argument("-r", "--reverse", help="频音的成生放倒", default=False, action="store_true")
	parser.add_argument("-n", "--norm", help="统一所有字音量", default=False, action="store_true")


	#新建活字印刷类实例
	HZYS = huoZiYinShua("./settings.json")

	args = parser.parse_args()

	#从文件读取输入
	if (args.file != ""):
		#读取要活字印刷的内容
		textFile = open(args.file, encoding="utf8")
		textToRead = textFile.read()
		textFile.close()
	#使用文本，不读取文件
	else:
		textToRead = args.text

	print("输出文本:" + textToRead)
	print("生成中...")


	#判定命令行参数，确定是否直接播放声音
	#直接播放
	if (args.directplay == True):
		print("直接播放")
		HZYS.directPlay(textToRead,
						inYsddMode=args.inYsddMode,
						pitchMult=float(args.pitchMult),
						speedMult=float(args.speedMult),
						reverse=args.reverse,
						norm=args.norm)
	#导出
	else:
		HZYS.export(textToRead,
					filePath=args.output,
					inYsddMode=args.inYsddMode,
					pitchMult=float(args.pitchMult),
					speedMult=float(args.speedMult),
					reverse=args.reverse,
					norm=args.norm)
	programPause = input("按下回车以退出...")
