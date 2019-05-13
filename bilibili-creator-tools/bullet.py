import codecs
import json
import operator
import os
import sys
# from typing import List
# import argparse
# import re
import time
from typing import *

import matplotlib.pyplot as plt
import numpy as np
import pyperclip
from bs4 import BeautifulSoup
from video import *

"""
aid_list: List[int], 整数格式的av号
"""
FILENAME = "tmp_danmu.csv"
MY_MID = 1769729  # 四眼井
TEST_AID = VideoPage(43006601)
TEST_CID = TEST_AID.cid_list[0]

header = {
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Referer': 'http://www.bilibili.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:45.0) Gecko/20100101 Firefox/45.0'
}


# todo: 美化生成图表, 增加更多(没什么卵用的)数据

def write_down(html, filename='test.html'):
    with open(filename, 'w') as f:
        f.write(html)


def get_bullets(cid, filename):
    bullet_api = "https://api.bilibili.com/x/v1/dm/list.so?oid="
    r2 = requests.get(bullet_api + cid, headers=header)
    soup = BeautifulSoup(r2.content, 'lxml')
    bullets = soup.find_all('d')
    with open(filename, 'w') as fw:
        print(u"写入弹幕ing...")
        for b in bullets:
            content = b.string
            attr = b['p'].split(',')
            t1 = str(attr[0])  # 视频中的时间
            t2 = attr[4]  # 发布时间
            # print(content.encode('utf-8').decode())
            timestr = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(t2)))
            fw.write(content.encode('utf-8').decode() + ',' + t1 + ',' + timestr + '\n')

    print(u"写入完成...请查看" + filename)


def _get_bullet_freq(cid: OnePage) -> Dict:
    """
    生成分p视频的弹幕频率字典
    :param cid: <OnePage>实例
    :return: Dict[秒数: 弹幕数]
    """
    print('cid{} 第{}P, 标题"{}" 获取弹幕频率... '.format(cid.c_int, cid.page, cid.c_title))

    time_list = _get_bullet_time(cid)
    time_list.sort()
    time_dict = {}
    if time_list:
        for i in range(int(time_list[-1] + 2)):
            time_dict[i] = 0
        for d in time_list:
            time_dict[int(d)] += 1
        max_bullet = max(time_dict.items(), key=operator.itemgetter(1))[0]
        print('共获取到{}条弹幕, 在{}秒最密集'.format(len(time_list), max_bullet))
    else:
        print("未获取到弹幕!")

    return time_dict


def _get_bullet_time(cid: OnePage) -> List[float]:
    """
    helper function
    :param cid: <OnePage> 实例
    :return: 每条弹幕在视频里的时间
    """

    bullet_api = "https://api.bilibili.com/x/v1/dm/list.so?oid="
    r2 = requests.get(bullet_api + str(cid.c_int), headers=header)
    # print(r2.content)
    soup = BeautifulSoup(r2.content, 'lxml')
    danmakus = soup.find_all('d')
    time_list = []

    for dan in danmakus:
        attr = dan['p'].split(',')
        t1 = attr[0]  # 视频中的时间
        time_list.append(float(t1))

    return time_list


def get_aid_list_from_json(filename, rank=None) -> List[int]:
    """读取 room.json文件, 生成弹幕热点图
    :param rank: 读取前多少项
    """
    aid_list = []
    data = json.load(codecs.open(filename, 'r', 'utf-8-sig'))
    for vids in data:
        aid_list.append(int(vids['编号']))

    return aid_list


def get_aid_list_from_clipboard() -> List[int]:
    """读取每行一个aid的剪贴板, 输出成List[aid]
    """
    clipboard_list = pyperclip.paste().split("\n")
    aid_list = []

    for line in clipboard_list:
        try:
            aid_list.append(int(line))
        except:
            pass
    return aid_list


# @pysnooper.snoop()
def get_popularity(target: VideoPage, show_img=True, mode: str = 'first') -> None:
    """
    生成视频的弹幕分布图
    :param aid: av号
    :param show_img: 生成后是否在桌面打开
    :param mode: 工作模式, 'all': 全部分p  'first': 第一个分p  '<cid号>': 指定分p
    :return: None
    """
    cid_list = []
    if mode == 'all':  # 生成所有分p
        cid_list = target.cid_list
    elif mode == 'first':  # 只生成第1p, cid为按顺序的第一个
        cid_list = [target.cid_list[0]]
    else:  # 生成指定cid的分析
        cid = int(mode)
        for this_cid in target.cid_list:
            if this_cid.c_int == cid:
                cid_list = [this_cid]

    print('===av{}, 生成分P数:{}==='.format(target.aid, len(cid_list)))

    for this_cid in cid_list:  # cid_list: List[OnePage]
        # print('当前cid:', c)
        freq_dict = _get_bullet_freq(this_cid)
        # print(freq_dict)
        img = _generate_freq_graph(this_cid, freq_dict)
        if show_img:
            openImage(img.replace('/', '\\'))
            # plt.show()
    return


def _generate_freq_graph(cid: OnePage, freq_dict: Dict) -> str:
    """
    生成单个cid的弹幕频率图
    :param target: aid类的对象
    :param cid: 分p号
    :param freq_dict: 上一步得到的弹幕频率
    :return: 保存文件的路径
    """
    if not freq_dict:
        print("生成失败, 可能原视频没有弹幕")
        return ''
    print('生成弹幕图像...')
    target = cid.video_page
    plt.figure(figsize=(20, 10))
    # plt.title(target.title, '  av{}, 分p号{}'.format(target.aid, c_int))
    plt.title(target.title)
    plt.xlabel("时间(秒)")
    plt.ylabel("弹幕数量")
    x_axis = []
    for i in freq_dict.keys():
        if i // 60 not in x_axis:
            # print(i)
            x_axis.append(i // 60)

    x = freq_dict.keys()
    if max(x) + 1 < 40:
        tick_interval = 1
    else:
        tick_interval = (max(x) + 1) // 40
    plt.xticks(np.arange(min(x), max(x) + 1, tick_interval))
    # plt.xticks(x_axis)
    plt.bar(x, freq_dict.values())

    dir = 'Graph/'
    if not os.path.exists(dir):
        os.makedirs(dir)

    clean_title = target.title.replace('/', '&').replace('.', '')
    file_name = "Graph/弹幕分布_av{}_{}_p{}.png".format(target.aid, clean_title, cid.page)
    print('完成! 保存到', file_name)
    plt.savefig(file_name)
    return file_name


def openImage(path):
    import subprocess
    imageViewerFromCommandLine = {'linux': 'xdg-open',
                                  'win32': 'explorer',
                                  'darwin': 'open'}[sys.platform]
    subprocess.run([imageViewerFromCommandLine, path])


def test():
    # _get_bullet_freq(75406617)
    # _get_bullet_time(75406617)
    # get_popularity(TEST_AID)
    # openImage('Graph\\弹幕分布_av43006601_【梦幻共演】和书记一起跳舞的奥尔加.png')
    # a = 'Graph/弹幕分布_av43006601_【梦幻共演】和书记一起跳舞的奥尔加.png'
    # openImage(a.replace('/', '\\'))
    get_popularity(19516333)

    bullet = _get_bullet_freq(TEST_CID)
    # print(bullet)
    pass


if __name__ == '__main__':
    # aid_list = get_aid_list_from_clipboard()
    # print('len', len(aid_list), '\ntype', type(aid_list[0]), aid_list)
    # for aid in aid_list:
    #     get_danmu_popularity(aid, True)
    test()
