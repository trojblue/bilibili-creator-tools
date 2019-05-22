from video import VideoPage, OnePage
import xlrd
from typing import Dict, List
import pyperclip
"""
自动化AE程序
todo:
 1. 读取excel文件
 2. 解决相对路径的问题
 3. 做出不带自动化的AE动画 (找人要到目前的ae文件)
 4. 制作demo, 发到群里
 5. 吸收问题, 修改并加入自动化解决方案
 
 
 大项目之间: 用 ||| (三竖线)分隔
 每个项目的同质小节之间: 用 /// (三斜线)分隔
 每小节的单元之间: 用 ^^^ (三上标) 分隔
 每单元的不同文本框: 用[[[ (三左方括号)分隔
"""
# todo:
#   0. 写完基本class结构 (读取excel)
#   1. 完成头像保存到本地
#   1.1. 把AE模板做好(不带自动化的)
#   2. 在ae里解决链接文字的问题
#   3. 加入自动化功能

#


class TopVideoes:
    """
    b站前20视频类, 用于生成AE自动化文件

    ===Attributes===
    excel: excel表格的位置
    vid_list: List[TopVideoPage]


    """
    def __init__(self, excel_file: str, top_count = 20):
        """
        :param excel_file: 需要读取的excel文件地址
        :param top_count: 生成前xx的视频
        """
        self.excel_file = excel_file
        self.top_count = top_count
        self.page_list = []
        for one_dict in self.get_info_dicts_from_excel():
            page = TopVideoPage(one_dict)
            self.page_list.append(page)

    def __repr__(self):
        return "<TopVideoes> Object: \n 文件地址:{}, 获取前{}个, \npage_list:{}".\
            format(self.excel_file, self.top_count, [i.title for i in self.page_list])


    def get_info_dicts_from_excel(self) -> List[Dict]:
        """读入ddtv的xlsx文件, 把信息和av号保存到List[Dict]文件
        """
        workbook = xlrd.open_workbook(self.excel_file, on_demand=True)
        page_sheet = workbook.sheet_by_index(0)


            # if worksheet.cell_value(colu, 0) == "分数":
            #     fed_dict['score']
        # print(page_sheet.cell_value(1, 1))
        totl = []

        for row in range (1, self.top_count+1): # by rank
            fed_dict = {}
            fed_dict['rank'] = row
            for colu in range(page_sheet.ncols):
                if page_sheet.cell_value(0, colu) == "分数":
                    fed_dict['score'] = page_sheet.cell_value(row, colu)
                elif page_sheet.cell_value(0, colu) == "标题":
                    fed_dict['title'] = page_sheet.cell_value(row, colu)
                elif page_sheet.cell_value(0, colu) == "AV号":
                    fed_dict['aid'] = int(page_sheet.cell_value(row, colu))

                elif page_sheet.cell_value(0, colu) == "总播放":
                    fed_dict['view'] = int(page_sheet.cell_value(row, colu))
                elif page_sheet.cell_value(0, colu) == "总喜欢":
                    fed_dict['like'] = int(page_sheet.cell_value(row, colu))
                elif page_sheet.cell_value(0, colu) == "总硬币":
                    fed_dict['coin'] = int(page_sheet.cell_value(row, colu))
                elif page_sheet.cell_value(0, colu) == "总收藏":
                    fed_dict['fav'] = int(page_sheet.cell_value(row, colu))

                elif page_sheet.cell_value(0, colu) == "本周增加播放":
                    fed_dict['view_gain'] = int(page_sheet.cell_value(row, colu))
                elif page_sheet.cell_value(0, colu) == "本周增加喜欢":
                    fed_dict['like_gain'] = int(page_sheet.cell_value(row, colu))
                elif page_sheet.cell_value(0, colu) == "本周增加硬币":
                    fed_dict['coin_gain'] = int(page_sheet.cell_value(row, colu))
                elif page_sheet.cell_value(0, colu) == "本周增加收藏":
                    fed_dict['fav_gain'] = int(page_sheet.cell_value(row, colu))
            totl.append(fed_dict)

        return totl



        pass

    def write_results(self):
        """输出结果到文件夹
        - 输出头像到/日期/avatar文件夹
        - 输出4项指标和增长值(方式未定)
        - 输出视频标题, av号, 投稿日期, 投稿人名字 (方式未定)
        """
        pass

    def get_avatar_links(self):
        """输出头像链接到剪贴板
        """
        all_link = ""
        for i in self.page_list:
            all_link += i.avatar + '\n'
        return all_link

class TopVideoPage(VideoPage):
    """周刊内的每个av号视频, 内容信从excel里提取

    ===Attributes===
    rank: 本周排行
    release_date: 发布日期
    score: 分数(来自excel)
    view: 播放量(来自excel)
    like: 点赞(来自excel)
    coin: 硬币(来自excel)
    fav: 收藏(来自excel)

    view_gain: 增加的播放量(来自excel)
    like_gain: 增加的点赞量(来自excel)
    coin_gain: 增加的硬币量(来自excel)
    fav_gain: 增加的收藏量(来自excel)

    aid: av号
    mid: 空间号
    a_title; 视频标题
    uploader: 投稿者名字
    """
    def __init__(self, info_dict: Dict):
        aid = info_dict["aid"]
        print("读取av{}信息...".format(aid))
        VideoPage.__init__(self, aid)
        self.rank = info_dict["rank"]
        self.score = info_dict["score"]
        self.score = info_dict["score"]

        self.view = info_dict["view"]
        self.like = info_dict["like"]
        self.coin = info_dict["coin"]
        self.fav = info_dict["fav"]
        self.view_gain = info_dict["view_gain"]
        self.like_gain = info_dict["like_gain"]
        self.coin_gain = info_dict["coin_gain"]
        self.fav_gain = info_dict["fav_gain"]

    def __repr__(self):
        basic_info = "<VideoPage> Object: av{}\n  title: {}\n  uploader: {}\n  c_int_list::{}\n  pub_date:{} \n". \
            format(self.aid, self.title, self.uploader, [c.c_int for c in self.cid_list], self.pub_date)
        return "<TopVideoPage> Object: \n ,{} \nrank: {}, score:{}".format(basic_info, self.rank, self.score)

    def write_result(self):
        """输出结果到文件夹
        - 输出头像到/日期/avatar文件夹
        - 输出4项指标和增长值(方式未定)
        - 输出视频标题, av号, 投稿日期, 投稿人名字 (方式未定)
        """
        pass



    def get_avatars(self, path: str):
        """
        下载前20排行视频的用户头像
        :param path:
        :return:
        """
        return self.avatar




def t_est():
    t = TopVideoes("sheet.xlsx", 5)
    print(t.get_avatar_links())

    print(t)

    # workbook = xlrd.open_workbook("sheet.xlsx", on_demand=True)
    # page_sheet = workbook.sheet_by_index(0)
    # for x in range (6):
    #     for y in range (page_sheet.ncols):
    #         print("x: {}, y:{}, {}".format(x, y, page_sheet.cell_value(x, y)))




if __name__ == '__main__':
    t_est()
























