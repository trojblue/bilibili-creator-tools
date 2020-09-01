# bilibili-creator-tools

chinese readme: → `readme.zh.md`

The project was made to assist the creation process of user-generated video contents.
It currently has **no** english translations.

Skills involved for this project:
- python spider (requests, beautifulSoup)
- PyQt 5 for making the GUI
- matplotlib for graph generation & styling

## Functions
1. downloading raw video from bilibili.com
2. fetch info for uploader and individual videos
3. generate histograms for danmaku intensity


## Usage
the exe version is available in the `dist` folder;

to run manually:

```Git
git clone https://github.com/Trojblue/bilibili-creator-tools.git
```

```python
pip install -r requirements.txt
python gui_driver.py
```



## Stucture

`bullet.py`: danmaku related functions

`video.py`: getting `aid` and `cid` from bilibili, and store fetched info as related objects 

`API.py`: connect the components to `gui_driver.py`

`gui_driver.py`: driver functions for GUI

`gui_v2.py`: PyQt5 generated GUI

`bili-tool.ui`: UI file for PyQt designer

sample outputs are available in `\doc`

## Screenshots
![pycharm64_2019-05-13_06-06-19.png](https://github.com/Trojblue/bilibili-creator-tools/blob/master/docs/pycharm64_2019-05-13_06-06-19.png?raw=true)

![pycharm64_2019-05-13_06-07-08.png](https://github.com/Trojblue/bilibili-creator-tools/blob/master/docs/pycharm64_2019-05-13_06-07-08.png?raw=true)




