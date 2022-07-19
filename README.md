".\dictionary.csv"里面可以定义非汉字字符的读法<br>
素材目录、词典目录、输入目录、输出目录在"settings.json"中编辑<br>
<br>
huoZiYinShua类里有两个方法：<br>
huoZiYinShua.export(rawData, filePath)<br>
	&emsp;&emsp;rawData为要阅读的文本（字符串）<br>
	&emsp;&emsp;filePath为保存的文件路径（字符串）<br>
<br>
huoZiYinShua.playText(rawData, tempPath = ".\\HZYSTempOutput\\temp.wav"):<br>
	&emsp;&emsp;rawData同上<br>
	&emsp;&emsp;tempPath为临时文件路径，可不填<br>
<br>
"main.exe"是打包好的程序，可直接运行<br>
效果：https://www.bilibili.com/video/BV1R541117uE
