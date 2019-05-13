# import json
# import subprocess
# import os
from typing import *

import requests

GET_VIDEO_LIST_URL = "https://space.bilibili.com/ajax/member/getSubmitVideos"
GET_VIDEO_INFO_URL = "https://api.bilibili.com/x/web-interface/view"
GET_VIDEO_DOWNLOAD_URL = "https://api.bilibili.com/x/player/playurl"
COOKIE = '_uuid=DD61A31E-67B8-A7EA-94E8-A7B012B0AD9E14426infoc; uuid=0f4d2e6c-c617-4583-83e4-8740aa9305f8; ' \
         'Hm_lvt_8a6e55dbd2870f0f5bc9194cddf32a02=1546726671,1547454704; ' \
         'CNZZDATA2724999=cnzz_eid%3D1834861307-1547711695-https%253A%252F%252Fwww.bilibili.' \
         'com%252F%26ntime%3D1549589184; LIVE_BUVID=AUTO4315498090132009; sid=ax9evfqg; fts=1549835071; ' \
         'buvid3=A42D65BE-F5AB-47C4-8BB0-EDCCA4DE10A66699infoc; CURRENT_FNVAL=16; im_notify_type_1769729=0; ' \
         'balh_server=https://biliplus.ipcjs.top; DedeUserID=1769729; DedeUserID__ckMd5=034fe41ef0150652; ' \
         'SESSDATA=2553aa40%2C1557624054%2Cd272d141; bili_jct=814c1c210735cb92b1ec8188d355f602; finger=b3372c5f; ' \
         'stardustvideo=1; rpdid=|(kJu)YR|k|R0J''ullY|uJmR|; im_local_unread_1769729=0; im_seqno_1769729=65166; ' \
         'bp_t_offset_1769729=251044854246214994; CURRENT_QUALITY=64; _dfcaptcha=3a719e85010b24ec57c69511651bdd5b'

"""
mid: up主空间号
aid： 即av号
c_int: 每个av号内的分p号
"""


# 已完成:
#   完善OOP结构
#   写完获取弹幕频率
#   图形化


# todo:
#  up主每日视频分析
#  标签搜索: 评价标签的热度
#  关键词搜索: 评价关键词的热度
#  评论 / 弹幕词云
#  评论 / 弹幕 情感分析
#  观看历史分析
#  (低优先) 视频收益预测
#  (低优先) 话题产生器
class Uploader:
    """单个up主

    === Public Attributes ===
    mid: up主空间id
    aid_list: 所有投稿视频av号
    name: UP主名称
    """

    def __init__(self, mid):
        self.mid = mid
        mid_json = self.get_mid_json()
        self.name = mid_json['data']['name']
        self.aid_list = self.get_aid_list()
        # todo: 完成每日信息采集逻辑

    def __repr__(self):
        return "mid{} \n  name: {} \n  videos: {}". \
            format(self.mid, self.name, self.aid_list)

    def collect_info(self) -> Dict:
        """统计本日信息, 写入到字典;
        'mid': self.mid
        'up_name':
        'av号': VideoPage
        """
        pass

    def write_json(self, filename):
        """把collect_info得到的数据写入到json
        """
        pass

    def get_aid_list(self) -> List[int]:
        """获取up主的所有投稿视频
        输入up主空间mid, 返回up主所有投稿的av号(aid)
        """
        mid = self.mid
        page_num = self.get_page_num()
        aid_list = []
        for page in range(1, page_num + 1):
            aid_list += self._get_page_aids(page)

        return aid_list

    def _get_page_aids(self, page: int) -> List[int]:
        """返回一页内的所有aid, helper function
        """
        mid = self.mid
        videoList = []
        response = requests.get(GET_VIDEO_LIST_URL,
                                {
                                    "mid": mid,
                                    "pagesize": 30,
                                    "tid": 0,
                                    "page": page,
                                    "keyword": "",
                                    "order": "pubdate"
                                }).json()
        # print(response)
        if response['status'] == True:
            datas = response['data']['vlist']
            for data in datas:
                videoList.append(data['aid'])
        return videoList

    def get_page_num(self) -> int:
        """
        返回up主空间内视频页数
        """
        mid = self.mid
        response = requests.get(GET_VIDEO_LIST_URL,
                                {
                                    "mid": mid,
                                    "pagesize": 30,
                                    "tid": 0,
                                    "page": 1,
                                    "keyword": "",
                                    "order": "pubdate"
                                }).json()
        return response['data']['pages']

    def get_mid_json(self) -> Dict:
        """
        获取up主个人信息, 主要内容在Dict['data']里
        :return: json,文件夹里有例子
        """
        try:
            headers = {
                'Connection': 'keep-alive',
                'Cookie': COOKIE,
                'Host': 'api.bilibili.com',
                'Referer': 'https://space.bilibili.com/' + str(self.mid),
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
            }
            url = 'https://api.bilibili.com/x/space/myinfo?jsonp=jsonp'
            # print('获取用户关注数量和粉丝数量url:{}'.format(url))
            req = requests.get(url, headers=headers, timeout=60)
            if req.status_code == 200:
                status = req.json()
                return status
            else:
                print('get_myinfo url失败 code:{}'.format(req.status_code))
        except ConnectionError as e:
            print('ConnectionError网络异常', e.args)


class VideoPage:
    """一个av号的视频

    === Public Attributes ===
    aid: av号
    mid: up主空间id
    cid_list: 分p视频的cid列表
    uploader: UP主名称
    a_title: 视频标题

    ===representation invariant===
    每个合法VideoPage至少有一个cid

    """

    def __init__(self, aid: int):
        """aid: av号"""
        self.aid = aid
        self.aid_json = self.get_aid_json()
        self.title = self.aid_json["title"]
        self.uploader = self.aid_json["owner"]["name"]
        self.mid = self.aid_json["owner"]["mid"]
        self.cid_list = self.get_cid_list()

    def __repr__(self):
        """返回av号 - 标题 - up主 - 分p"""
        return "<VideoPage> Object: av{}\n  title: {}\n  uploader: {}\n  c_int_list::{}\n". \
            format(self.aid, self.title, self.uploader, [c.c_int for c in self.cid_list])

    def info(self) -> Dict:
        """把单个视频的信息返回到上级, 用于统计每天的变化
        返回: 播放, 点赞, 硬币, 分享,
        """
        pass

    def get_cid_list(self) -> List:
        """返回单个av号内的所有分p号
        >>> a = VideoPage(1769729)
        >>> a.get_cid_list()
        [2707975, 2707976, 2707977]
        """
        cid_list = []
        for i in self.aid_json['pages']:  # 每个i对应一个cid
            the_cid, page, c_title = i['cid'], i['page'], i['part']
            c = OnePage(self, the_cid, page, c_title)

            cid_list.append(c)

        return cid_list

    def get_aid_json(self) -> Dict:
        """
        返回<av号>视频的json, 可能包含多个分p (c_int)
        样例:见文件夹内json样本
        """
        aid = self.aid
        response = requests.get(GET_VIDEO_INFO_URL, {
            "aid": aid
        }).json()
        # print(response)
        if response['code'] == 0:
            # print(response['data'])
            return response['data']

        # print(response['data'])


class OnePage:
    """一个视频的一个分p

    === Public Attributes ===
    aid: 从属aid
    c_int: 分p号
    video_page: 从属VideoPage
    c_title: 分p标题
    """

    # todo: 增加完整分辨率下载功能 https://github.com/Henryhaohao/
    #  Bilibili_video_download/blob/master/downloader_v1.py

    def __init__(self, video_page, cid, page, title):
        self.video_page = video_page
        self.aid = self.video_page.aid
        self.c_int = cid  # 数字格式的cid
        self.c_title = title  # 分p标题
        self.page = page  # 分p编号, 从1开始

    def __repr__(self):
        return "<OnePage> Object: cid{}, av{}, c_title={}". \
            format(self.c_int, self.video_page.aid, self.c_title)

    def get_download_url(self, qn=80) -> str:
        """返回av号内单个分p(c_int)的下载链接
        """
        aid = self.aid
        cid = self.c_int
        response = requests.get(GET_VIDEO_DOWNLOAD_URL, {
            'avid': aid,
            'c_int': cid,
            'qn': 80,
            'otype': 'json',
            'fnver': 0,
            'fnval': 16
        }).json()
        if response['code'] == 0:
            # print(response)
            return response['data']['dash']['video']

    def info(self):
        pass

    def get_bullet_popularity(self):
        pass


TEST_AID = VideoPage(43006601)
TEST_CID = TEST_AID.cid_list[0]


# @pysnooper.snoop()
def test():
    a = VideoPage(19516333)
    print(a.cid_list[0])

    # four_well = Uploader(1769729)
    # print(four_well)


def main():
    pass


if __name__ == "__main__":
    test()
    # main()
    # OG_code()
    # print('请在main内打开!')
