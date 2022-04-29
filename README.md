".\dictionary.csv"里面可以定义非汉字字符的读法<br>
".\素材\"为活字印刷素材的存放目录，音频素材需全部命名为"{对应拼音}.wav"<br>
<br>
huoZiYinShua类里有两个方法：<br>
huoZiYinShua.export(rawData, filePath)<br>
	&emsp;&emsp;rawData为要阅读的文本（字符串）<br>
	&emsp;&emsp;filePath为保存的文件路径（字符串）<br>
<br>
playtext(rawData, tempPath = ".\\HZYSTempOutput\\temp.wav"):<br>
	&emsp;&emsp;rawData同上<br>
	&emsp;&emsp;tempPath为临时文件路径，可不填<br>
<br>
具体使用示例见".\main.py"
