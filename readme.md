# bilibili-creator-tools

适用于b站up主的创作辅助工具   **未完成**

## 功能

这个项目主要是练手用的, 目前有两个功能:

1. 下载b站视频
2. 分析视频弹幕频率

界面上总共分了4页, 但能用的只有上面两个功能(逃)

目前在做第三个功能AE自动化, 适用于自动制作周刊排名类的视频



## 结构

`bullet.py`: 提供弹幕相关功能

`video.py`: 从b站抓取up主/视频(aid)/视频分页(cid)信息, 并创建实例

`API.py`: 整合以上文件, 并提供给gui_driver.py

`gui_driver.py`: 图形界面的驱动程序

`gui_v2.py`: PyQt5生成的图形界面

`QSSWhite.py`: 美化界面用的QSS文件

`bili-tool.ui`: PyQt Designer使用的ui文件

在`\doc`文件夹里有图形界面和输出格式的例子



## 安装

在`dist`目录里有编译好的windows版:`v0.1.rar`

安装Python3.7和必要的库:

```python
pip install -r requirements.txt
```

下载项目:
```Git
git clone https://github.com/Trojblue/bilibili-creator-tools.git
```



## 使用

启动图形GUI:

1. CMD 切换到当前目录`bilibili-creator-tools`
2. 在 CMD 里输入: `python gui_driver.py`

GUI大概长这样
![pycharm64_2019-05-13_06-06-19.png](https://github.com/Trojblue/bilibili-creator-tools/blob/master/docs/pycharm64_2019-05-13_06-06-19.png?raw=true)

![pycharm64_2019-05-13_06-07-08.png](https://github.com/Trojblue/bilibili-creator-tools/blob/master/docs/pycharm64_2019-05-13_06-07-08.png?raw=true)


## FAQ

- 生成的图像里中文是乱码: [source](<https://segmentfault.com/a/1190000005144275>)

> ```python
> import matplotlib
> matplotlib.matplotlib_fname() #将会获得matplotlib包所在文件夹
> ```
>
> 1.在Windows/fonts文件夹选择SimHei字体（也就是“黑体常规”），将其复制到matplotlibmpl-datafontsttf文件夹下
> 2.打开matplotlibrc配置文件，把font.family改成simhei（注意去掉前面的#号）
> 3.重新执行"启动"步骤



- 其他问题: 检测是否已安装所有需要的库; 检测python版本(我是3.7.0)
- 几乎可以肯定还有很多其他bug, 欢迎联系我: `四眼井 QQ570879411`



## 致谢

这个小工具主要的用处是练习上手PyQt5, 参考了很多Git和互联网上的内容, 感谢各位大佬提供的教程和代码(小声)

















