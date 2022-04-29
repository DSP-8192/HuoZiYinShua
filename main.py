from huoZiYinShua import *


if __name__ == "__main__":
	HZYS = huoZiYinShua(".\\素材\\", ".\\dictionary.csv")
	HZYS.export("从未有过如此美妙的开局", ".\\Output.wav")
	HZYS.playtext("污渍yyds")
	
