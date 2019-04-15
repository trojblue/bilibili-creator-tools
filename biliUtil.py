import requests
import json
import subprocess
import os
from typing import *

GET_VIDEO_LIST_URL = "https://space.bilibili.com/ajax/member/getSubmitVideos"
GET_VIDEO_INFO_URL = "https://api.bilibili.com/x/web-interface/view"
GET_VIDEO_DOENLOAD_URL = "https://api.bilibili.com/x/player/playurl"

def getVideos(mid:int, page) -> List:

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


def getVideoList(mid, page_num):
    """
    返回<mid>空间内的所有aid (视频号)
    """
    list = []
    for page in range(1, page_num+1):
        # print(page)
        videos = getVideos(mid, page)
        for video in videos:
            list.append(video)
    return list


def getVideoPageNum(mid):
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


def getVideoPages(aid):
    """
    返回视频信息页的json
    """
    response = requests.get(GET_VIDEO_INFO_URL, {
        "aid": aid
    }).json()
    # print(response)
    if response['code'] == 0:
        return response['data']


def getDownloadUrl(aid, cid, qn=80):
    respone = requests.get(GET_VIDEO_DOENLOAD_URL, {
        'avid': aid,
        'cid': cid,
        'qn': 80,
        'otype': 'json',
        'fnver':0,
        'fnval':16
    }).json()
    if respone['code'] == 0:
        #print(respone)
        return respone['data']['dash']['video']

def downloadVideo(aid,url,title):
    referer = 'https://www.bilibili.com/video/av'+str(aid)
    downShell = './aria2/aria2c '+' -s 5 -o\'files/'+title+'.flv\' --referer='+ referer+' \'' + url+ '\''
    subprocess.Popen([r'powershell',downShell])

def OG_code():
    print("=== 写这段代码的时候，只有上帝和我知道它是干嘛的  ===")
    print("=== 现在，只有上帝知道 ===")
    print("=== 希望您用的时候不要踩坑，虽然不可能 ===")
    print("")
    mid = 1769729
    print("=== your space number is " + str(mid) + " ===")
    # os.system('pause')

    pageNum = getVideoPageNum(mid)
    print(pageNum)
    print("===get ", pageNum, " pages of videos===")
    videoList = getVideoList(mid, pageNum)
    # print(videoList)
    lenV = len(videoList)

    os.system('pause')
    for i in range(0, lenV):
        video = getVideoPages(videoList[i])
        title = video['title']
        aid = videoList[i]
        pages = video['pages']
        print("===downloading video " + str(i + 1) + ' of ' + str(lenV) + "===")

        for i in range(0, len(pages) - 1):
            url = getDownloadUrl(aid, pages[i]['cid'])
            downloadVideo(aid, url[len(url) - 1]['baseUrl'], title + '-P' + str(i))

    print("===all videos downloaded~~~===")


def testing():
    aid = 44434402
    video = getVideoPages(aid)
    title = video['title']
    pages = video['pages']
    url = getDownloadUrl(aid, pages[0]['cid'])
    print(aid, '\n', video, '\n', title,  '\n',pages,  '\n',url)

    downloadVideo(aid, url[len(url) - 1]['baseUrl'], title + '-P')

if __name__ == "__main__":

    # OG_code()
    testing()

