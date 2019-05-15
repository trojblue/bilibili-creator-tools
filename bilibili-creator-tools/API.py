# -*- coding: utf-8 -*-

import json
import os
import re
import subprocess
from typing import Tuple

import bullet
import requests
import you_get
from bs4 import BeautifulSoup as bs
from video import VideoPage


# class you_brew(you_get):
#
#     def download(self):
#         start_url = 'https://www.bilibili.com/video/av51913907/'
#         self.any_download(utl=start_url)

class API(object):
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                                      ' (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
        self.headers_m = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 '
                                        '(KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1'}

    def getmsg(self, themsg, thecolor):
        """形成富文本，参数是文本内容和字体颜色
        """
        msg = '<html><head/><body><p><span style=" font-family:Microsoft YaHei;font-size:9pt; color:{};">{}</span></p></body></html>'.format(
            thecolor, themsg)
        return msg

    # @pysnooper.snoop()

    # 从文件读取信息，返回一个列表
    def get_Infos(self, filename):
        Infos = []
        with open(filename, 'r') as f:
            data = f.readlines()
        for each in data:
            if len(each.strip()) > 0:
                Infos.append(each.strip())
        return Infos

    # 获取单个天猫商品DSR
    def get_TM(self, id, outfile):
        url = 'https://dsr-rate.tmall.com/list_dsr_info.htm?itemId=%s' % id
        res = requests.get(url, headers=self.headers)
        html = res.text
        date = re.findall('json.*?\((.*)\)', html)[0]
        dsr = json.loads(date)['dsr']  # 转换成字典格式
        DSR = id + ',' + str(dsr['gradeAvg']).strip() + ',' + str(dsr['rateTotal']).strip()
        with open(outfile, 'a') as f:
            f.write(DSR + '\n')
        return

    # 获取单个京东商品DSR
    def get_JD(self, id, outfile):
        url = 'https://club.jd.com/comment/productCommentSummaries.action?referenceIds=%s' % id
        res = requests.get(url, headers=self.headers)
        html = res.text
        dic = json.loads(html)['CommentsCount'][0]
        SkuId = str(dic['SkuId']).strip()  # 商品ID
        GoodRate = str(dic['GoodRate']).strip()  # 好评率
        GoodCount = str(dic['GoodCount']).strip()  # 好评数
        GeneralCount = str(dic['GeneralCount']).strip()  # 中评数
        PoorCount = str(dic['PoorCount']).strip()  # 差评数
        DSR = SkuId + ',' + GoodRate + ',' + GoodCount + ',' + GeneralCount + ',' + PoorCount
        with open(outfile, 'a') as f:
            f.write(DSR + '\n')
        return

    # 获取天猫主图链接和价格
    def getimglink(self, ID, outfile):
        # 打开手机端网页
        url = "https://detail.m.tmall.com/item.htm?id={}".format(ID)
        html = requests.get(url, headers=self.headers_m).text
        try:
            soup = bs(html, "lxml")
            imglink = "https:" + soup.select("div.itbox > a > img")[0].get("src")
        except:
            imglink = "miss"
        infos = re.findall('"price":"(\d+?\.\d\d)"', html)
        try:
            maxprice = max(list(map(float, infos)))
            minprice = min(list(map(float, infos)))
        except ValueError:
            maxprice = max(infos)
            minprice = min(infos)
        except:
            maxprice = "miss"
            minprice = "miss"
        thestr = ",".join([str(ID), imglink, str(maxprice), str(minprice)])
        with open(outfile, "a") as f:
            f.write(thestr + "\n")


# 输出富文本消息
def getmsg(themsg, thecolor='#464749'):
    """形成富文本，参数是文本内容和字体颜色
    """
    msg = '<html><head/><body><p><span style=" font-family:Microsoft YaHei;font-size:9pt; color:{};">{}</span></p></body></html>'.format(
        thecolor, themsg)
    return msg


def get_input_aid(raw_aid: str) -> Tuple:
    """
    从用户输入获取需要的aid
    :return: List[aid] + bool:用户输入是否符合规范
    """
    a_list = raw_aid.strip(' ').replace(" ", "").replace("av", "").replace("，", ",").split(',')  # 去除空格/av, 替换中文逗号
    try:
        bullet_aids = [int(i) for i in a_list]
        if not a_list:
            return ([], False)
        else:
            return (bullet_aids, True)
    except:
        Exception()
        print('不符合av号格式, 尝试使用url...')
        return (raw_aid, False)

def open_explorer(path: str = ''):
    """
    用文件浏览器打开文件夹下的相对路径
    :param path: 文件夹名称(ex.'\\Graph')
    :return: None
    """
    abs_path = os.path.abspath(__file__)
    abs_dir = os.path.split(abs_path)[0] + path
    subprocess.Popen('explorer {}'.format(abs_dir))

def get_abs_dir():
    """输出绝对地址, 比如
    D:\Python\Personal\bilibili-creator-tools-dev\bilibili-creator-tools
    """
    abs_path = os.path.abspath(__file__)
    abs_dir = os.path.split(abs_path)[0]
    return abs_dir

# 下载1080p视频
def download_video(target: VideoPage, mode: str = 'first', merge=True, save_bullet=False):
    """
    在you-get包的__main__加上这个def:
    def download(url, save_to, merge=True, save_bullet=False):
        from .common import any_download
        any_download(url=url)
    """
    # start_url = 'https://api.bilibili.com/x/web-interface/view?aid={}/?p=1'.format(target.aid)
    a = you_get
    dir = get_abs_dir()

    start_url = "https://www.bilibili.com/video/av{}/".format(target.aid)
    a.download(start_url, dir + '\\Video')

# 生成弹幕热度 from bullet.py
def get_popularity(target: VideoPage, show_img=True, mode: str = 'first') -> None:
    """
    生成视频的弹幕分布图
    :param aid: av号
    :param show_img: 生成后是否在桌面打开
    :param mode: 工作模式, 'all': 全部分p  'first': 第一个分p  '<cid号>': 指定分p
    :return: None
    """
    bullet.get_popularity(target, show_img, mode)


def test():
    # target = VideoPage(52068429)
    # download_video(target)

    a = get_input_aid('46545654')
    print(a)

    # a.download(start_url, get_abs_dir())    # url, 地址, 修改了youget库
    # pass
    # print("av123, av3asd阿萨德456，av987".replace(" ", "").replace("av", "").replace("，", ","))
    # a = you_brew
    # a.download(start_url)


if __name__ == '__main__':
    test()
    # print(get_abs_dir())
