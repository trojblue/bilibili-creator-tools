# 获取弹幕频率:

## 未完成版本

==离完成版还早, 目前是未完成版本==



## 介绍

QQ: `570879411 四眼井`

DDTV视频制作用, 负责生成`room.json`内所有视频的弹幕热度图

使用前请安装Python3.7和必要的库:

```python
pip install numpy --user
pip install matplotlib --user
```



## 启动

1. CMD 切换到当前目录
2. 在 CMD 里输入:

```python
python Main.py
```

3. 回车, 图片会生成在`Graph` 目录里



## FAQ

- `no such file or directory`: 在根目录下手动创建"Graph" 文件夹
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



## 致谢

用到的项目:

> <https://github.com/qq519043202/BILI/blob/master/danmuku.py>
>
> <https://segmentfault.com/a/1190000017511459>













# ShorterBilibili
