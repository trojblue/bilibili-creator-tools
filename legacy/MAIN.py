import codecs
import json

import matplotlib.pyplot as plt
import numpy as np
from biliUtil import *
from danmu import *

"""
aid_list: List[int], 整数格式的av号
"""
FILENAME = "tmp_danmu.csv"
MY_MID = 1769729  # 四眼井


def get_int_danmu(time_list) -> Dict:
    """返回(时间, 弹幕数)
    假设time_list sorted
    """
    time_dict = {}
    for i in range(int(time_list[-1] + 1)):
        time_dict[i] = 0

    for d in time_list:
        time_dict[int(d)] += 1

    return time_dict


def get_danmu_popularity(aid: int, show_img=True) -> None:
    """生成<aid>视频的弹幕的时间热度分析
    show_img: 是否显示刚生成的图像
    """
    aid = str(aid)
    cid = get_cid(aid)
    title = getVideoPages(aid)['title']

    time_list = [float(i) for i in get_danmuku_time(cid, FILENAME)]
    time_list.sort()
    per_sec_dict = get_int_danmu(time_list)

    print('av' + aid, title, "获取到 %s 条弹幕" % (str(len(time_list))))
    print("生成弹幕分布... ")

    # plt.bar((len(time_list)), time_list)
    plt.figure(figsize=(20, 10))
    plt.title(title)
    plt.xlabel("时间(秒)")
    plt.ylabel("弹幕数量")
    x_axis = []
    for i in per_sec_dict.keys():
        if i // 60 not in x_axis:
            # print(i)
            x_axis.append(i // 60)

    x = per_sec_dict.keys()
    if max(x) + 1 < 40:
        tick_interval = 1
    else:
        tick_interval = (max(x) + 1) // 40
    plt.xticks(np.arange(min(x), max(x) + 1, tick_interval))
    # plt.xticks(x_axis)
    plt.bar(x, per_sec_dict.values())

    dir = 'Graph/'
    if not os.path.exists(dir):
        os.makedirs(dir)

    clean_title = title.replace('/', '&').replace('.', '')
    # file_name = 'Graph/' + '弹幕分布_av' + str(aid) + '_' + clean_title + '.png'
    file_name = 'Graph/' + '弹幕分布_av' + str(aid) + '_' + '.png'
    plt.savefig(file_name)
    # plt.savefig('graph/graph.png')
    print("完成! 保存到", file_name)
    if show_img:
        plt.show()

    # plt.close()


def get_aid_list_from_json(filename, rank=None) -> List[int]:
    """读取 room.jeon文件, 生成弹幕热点图"""
    aid_list = []

    data = json.load(codecs.open(filename, 'r', 'utf-8-sig'))
    for vids in data:
        aid_list.append(int(vids['编号']))

    return aid_list


def get_aid_list_from_clipboard() -> List[int]:
    """读取每行一个aid的剪贴板, 输出成List[aid]
    """
    import pyperclip

    clipboard_list = pyperclip.paste().split("\n")
    aid_list = []

    for line in clipboard_list:
        try:
            aid_list.append(int(line))
        except:
            pass

    return aid_list


if __name__ == '__main__':
    # page = get_page_num(MY_MID)
    # vid_list = getVideoList(MY_MID, page)
    # for v in vid_list:
    #     get_danmu_popularity(v, False)

    # get_danmu_popularity(45917698, False)
    # get_danmu_popularity(46909295, False)

    aid_list = get_aid_list_from_clipboard()
    # print('len', len(aid_list), '\ntype', type(aid_list[0]), aid_list)
    for aid in aid_list:
        get_danmu_popularity(aid, True)
