# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets
from gui_v2 import Ui_MainWindow
import sys
import API as api
import time
from video import VideoPage, Uploader
import pysnooper

TEST_AIDS = [600781, 3357900, 17405257]


class MainUI(Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.aboutmsg = "适用于B站up主的综合投稿分析工具, 目前只做了2个功能, 绝赞更新中\n\n" \
                        "这软件也顺带作为DDTV的周刊制作工具使用(自动化AE的功能)\n\n" \
                        "如果爬虫失效程序会报错退出，要是程序无法继续使用的话请联系我!!\n\n" \
                        "<Python做桌面程序简直太痛苦了>\n" \
                        "bilibili-creator-tools v0.1\n"
        self.authormsg = "作者：四眼井\n\nB站: https://space.bilibili.com/1769729\n\n如果对本款小工具有疑问或者发现Bug，" \
                         "请和我联系\n\nQQ：570879411\n"

        self.actionOpenfile.triggered.connect(self.startExplorer)  # 打开当前文件夹
        self.actionQiut.triggered.connect(self.close)  # 菜单栏退出按钮函数
        self.actionAbout.triggered.connect(lambda: self.selectInfo("关于软件", self.aboutmsg))  # 关于软件
        self.actionAuthor.triggered.connect(lambda: self.selectInfo("作者", self.authormsg))  # 关于作者
        self.pushButton_1.clicked.connect(self.startdsr)  # DSR开始按钮
        self.pushButton_2.clicked.connect(self.startlink)  # 下载视频开始按钮
        self.pushButton_3.clicked.connect(self.startimg)  # 批量下载图片开始按钮

    # 重写关闭函数
    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, '关闭程序',
                                               "关闭程序可能导致正在进行的操作终止，请确认\n是否退出并关闭程序？",
                                               QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    # def downloadOptions(self):
    #     """下载视频页里的3个复选框: 分别为
    #     open_folder, get_bullet, merge_parts
    #     """
    #
    #     open_folder, get_bullet, merge_parts = True
    #     if not self.checkBox_2.isChecked():
    #         open_folder = False
    #     if not self.checkBox_5.isChecked():
    #         get_bullet = False
    #     if not self.checkBox_6.isChecked():
    #         merge_parts = False
    #     return (open_folder, get_bullet, merge_parts)

    # 消息框函数，传入2个参数，第1个是标题，第2个是显示内容
    def selectInfo(self, thetitle, megs):
        QtWidgets.QMessageBox.about(self, thetitle, megs)

    # 提取DSR中商品类型
    def changePD(self):
        if self.radioButton_1.isChecked():
            product = "tmall"
        if self.radioButton_2.isChecked():
            product = "jingdong"
        return product

    # 更新状态栏
    def statusshow(self, astr):
        self.statusbar.showMessage(astr)

    # DSR槽函数---------------------------------------------------------------------------------------------------
    # 启动DSR线程的槽函数
    def startdsr(self):
        self.statusbar.setStyleSheet("color:green")
        self.pushButton_1.setDisabled(True)  # 线程启动锁定按钮
        self.textEdit_1.setText("")  # 插入一个空白，每次启动线程都可以清屏
        txtname = self.lineEdit_1.text()
        product = self.changePD()
        self.dsrthread = dsrThread(txtname, product)
        self.dsrthread.status_signal.connect(self.statusshow)
        self.dsrthread.dsrtext_signal.connect(self.dsrtextshow)
        self.dsrthread.dsrprogmax_signal.connect(self.dsrprog_max)
        self.dsrthread.dsrprog_signal.connect(self.dsrprog_value)
        self.dsrthread.finished.connect(self.dsrpushon)  # 线程结束执行函数
        self.dsrthread.start()

    # 线程结束后开启DSR按钮
    def dsrpushon(self):
        self.pushButton_1.setDisabled(False)

    # 更新DSR输出文本
    def dsrtextshow(self, astr):
        self.textEdit_1.append(astr)

    # 获取DSR进度条最大值
    def dsrprog_max(self, n):
        self.progressBar_1.setMinimum(0)
        self.progressBar_1.setMaximum(n)

    # 更新DSR进度条
    def dsrprog_value(self, i):
        self.progressBar_1.setValue(i)

    # 主图链接槽函数------------------------------------------------------------------------------------------------

    def startlink(self):
        print('start download mode')
        self.statusbar.setStyleSheet("color:blue")
        print('1')
        self.pushButton_2.setDisabled(True)  # 线程启动锁定按钮
        self.textEdit_2.setText("")  # 插入一个空白，每次启动线程都可以清屏
        print('2')
        raw_aids = self.lineEdit_2.text()
        print('rawaidsishere', raw_aids)
        # options = self.downloadOptions()
        self.linkthread = linkThread(raw_aids)
        self.linkthread.status_signal.connect(self.statusshow)
        self.linkthread.linktext_signal.connect(self.linktextshow)
        self.linkthread.progmax_signal.connect(self.linkprog_max)
        self.linkthread.progvalue_signal.connect(self.linkprog_value)
        self.linkthread.finished.connect(self.linkpushon)  # 线程结束执行函数
        self.linkthread.start()

    def startExplorer(self):
        api.open_explorer()

    def linkpushon(self):
        self.pushButton_2.setDisabled(False)

    def linktextshow(self, astr):
        self.textEdit_2.append(astr)

    def linkprog_max(self, n):
        self.progressBar_2.setMinimum(0)
        self.progressBar_2.setMaximum(n)

    def linkprog_value(self, i):
        self.progressBar_2.setValue(i)

    # 批量下载图片槽函数----------------------------------------------------------------------------------------------

    def startimg(self):
        self.statusbar.setStyleSheet("color:green")
        self.pushButton_3.setDisabled(True)  # 线程启动锁定按钮
        self.textEdit_3.setText("")  # 插入一个空白，每次启动线程都可以清屏
        raw_aids = self.lineEdit_31.text()
        print('raw_aids:', raw_aids)
        aids = api.get_input_aid(raw_aids)
        print('processed', aids)
        self.imgthread = imgThread(aids)
        if aids[1] == False:
            self.pushButton_3.setDisabled(False)
        else:
            # imgfile = self.lineEdit_32.text()

            self.imgthread.status_signal.connect(self.statusshow)
            self.imgthread.imgtext_signal.connect(self.imgtextshow)
            self.imgthread.progmax_signal.connect(self.imgprog_max)
            self.imgthread.progvalue_signal.connect(self.imgprog_value)
            self.imgthread.finished.connect(self.imgpushon)  # 线程结束执行函数
            self.imgthread.start()

    def imgpushon(self):
        self.pushButton_3.setDisabled(False)

    def imgtextshow(self, astr):
        self.textEdit_3.append(astr)

    def imgprog_max(self, n):
        self.progressBar_3.setMinimum(0)
        self.progressBar_3.setMaximum(n)

    def imgprog_value(self, i):
        self.progressBar_3.setValue(i)


# DSR线程

class dsrThread(QtCore.QThread):
    status_signal = QtCore.pyqtSignal(str)  # 发送给状态栏的信号
    dsrtext_signal = QtCore.pyqtSignal(str)  # 发送给DSR输出框的信号
    dsrprogmax_signal = QtCore.pyqtSignal(int)  # 发送给进度条的信号，给出最大值
    dsrprog_signal = QtCore.pyqtSignal(int)  # 发送给进度条的信号，给出每次刷新的进度

    def __init__(self, txtname, product):  # 参数：读取的文件名，商品类型
        super().__init__()
        self.txtname = txtname
        self.product = product
        self.api = api.API()

    def run(self):
        self.dsrtext_signal.emit(api.getmsg("这部分还没做完", "red"))
        # start = time.time()
        # T = datetime.datetime.now()
        # self.status_signal.emit("当前状态：正在进行DSR提取操作...")
        # try:
        #     IDs = self.api.get_Infos(self.txtname)
        # except:
        #     self.dsrtext_signal.emit(self.api.getmsg("读取文件失败，请检查文件名称是否有误！", "red"))
        # else:
        #     nums = len(IDs)
        #     self.dsrprogmax_signal.emit(nums)
        #     i = 1
        #     if self.product == "tmall":
        #         outfile = "TMdsr_" + T.strftime("%Y%m%d%H%M") + "_" + str(nums) + ".csv"
        #         self.dsrtext_signal.emit(self.api.getmsg("商品类型为【天猫商品】，有效ID总计{}个，开始提取DSR".format(nums), "#464749"))
        #         with open(outfile, 'w') as f:
        #             f.write('商品ID,评分,评论数\n')
        #         for each in IDs:
        #             try:
        #                 self.api.get_TM(each, outfile)
        #             except:
        #                 msg_b = "总计{}个商品ID,第{}个商品：{}写入信息失败！".format(nums, i, each)
        #                 self.dsrtext_signal.emit(self.api.getmsg(msg_b, "red"))
        #             else:
        #                 msg_c = "总计{}个商品ID,成功写入第{}个天猫商品：{}".format(nums, i, each)
        #                 self.dsrtext_signal.emit(self.api.getmsg(msg_c, "#464749"))
        #                 self.dsrprog_signal.emit(i)
        #             i += 1
        #     elif self.product == "jingdong":
        #         outfile = "JDdsr_" + T.strftime("%Y%m%d%H%M") + "_" + str(nums) + ".csv"
        #         self.dsrtext_signal.emit(self.api.getmsg("商品类型为【京东商品】，有效ID总计{}个，开始提取DSR".format(nums), "#464749"))
        #         with open(outfile, 'w') as f:
        #             f.write('SKUID,好评率,好评数,中评数,差评数\n')
        #         for each in IDs:
        #             try:
        #                 self.api.get_JD(each, outfile)
        #             except:
        #                 msg_b = "总计{}个商品ID,第{}个商品：{}写入信息失败！".format(nums, i, each)
        #                 self.dsrtext_signal.emit(self.api.getmsg(msg_b, "red"))
        #            else:
        #                 msg_c = "总计{}个商品ID,成功写入第{}个京东商品：{}".format(nums, i, each)
        #                 self.dsrtext_signal.emit(self.api.getmsg(msg_c, "#464749"))
        #                 self.dsrprog_signal.emit(i)
        #             i += 1
        #     end = time.time()
        #     msg_d = "DSR提取完毕，耗时：%0.2f秒！\n数据保存在当前目录下表格  %s  中" % (float(end - start), outfile)
        #     self.dsrtext_signal.emit(self.api.getmsg(msg_d, "green"))
        # self.status_signal.emit("当前状态：DSR信息提取操作完毕！")


class linkThread(QtCore.QThread):
    status_signal = QtCore.pyqtSignal(str)
    linktext_signal = QtCore.pyqtSignal(str)
    progmax_signal = QtCore.pyqtSignal(int)
    progvalue_signal = QtCore.pyqtSignal(int)

    def __init__(self, raw_aid):
        super().__init__()
        self.raw_aid = raw_aid
        # self.open_folder =  options[0]
        # self.save_bullets = options[1]
        # self.merge = options[2]

        # print('raw_aid', raw_aid)

    @pysnooper.snoop()
    def run(self):
        """两种模式: 获取av号批量下载, 或者从连接下载"""
        aid_tuple = api.get_input_aid(self.raw_aid)
        if aid_tuple[1] == False:  # 不合法或者是URL
            self.run_url()
        else:  # 批量av号输入
            self.aid_list = aid_tuple[0]
            self.run_aid()

    def run_url(self):
        """aid运行模式"""
        print('使用url模式')
        start = time.time()
        self.status_signal.emit("当前状态：解析视频...")
        self.progmax_signal.emit(1)
        msg_b = '使用URL模式开始下载...请在命令行查看进度'
        self.linktext_signal.emit(api.getmsg(msg_b, "#464749"))

        self.progvalue_signal.emit(0)
        api.download_video(self.raw_aid)
        self.linktext_signal.emit(api.getmsg('已完成', "green"))

        self.progvalue_signal.emit(1)

        f = float(time.time() - start)
        out_time = '%.2f' % f
        msg_d = "下载完成，耗时{}秒;\n所有视频保存在/Video文件夹中".format(out_time)
        self.linktext_signal.emit(api.getmsg(msg_d, "green"))
        # if self.open_folder:
        try:
            api.open_explorer('\\Video')
        except:
            Exception()
            self.linktext_signal.emit(api.getmsg('打开文件夹失败, 请自行查看图像', "red"))

        self.status_signal.emit("当前状态：视频下载完成！")

    @pysnooper.snoop()
    def run_aid(self):
        """aid运行模式"""
        start = time.time()
        self.status_signal.emit("当前状态：解析视频...")
        aid_count = len(self.aid_list)
        self.progmax_signal.emit(aid_count)
        msg_b = '获取av号总计{}个，开始批量下载...'.format(aid_count)
        self.linktext_signal.emit(api.getmsg(msg_b, "#464749"))
        if aid_count == 1:  # 单个视频
            self.progvalue_signal.emit(0)
            one_aid = VideoPage(self.aid_list[0])
            self.linktext_signal.emit(api.getmsg('开始下载视频...av{} {}, 请在命令行查看进度'. \
                                                 format(one_aid.aid, one_aid.title), "#464749"))
            api.download_video(one_aid)
            self.linktext_signal.emit(api.getmsg('已完成: av{}'.format(one_aid.aid), "green"))
        else:  # 多个视频
            for i in range(aid_count):
                self.progvalue_signal.emit(i)
                one_aid = VideoPage(self.aid_list[i])
                self.linktext_signal.emit(api.getmsg('开始下载视频...av{} {}, 请在命令行查看进度'. \
                                                     format(one_aid.aid, one_aid.title), "#464749"))
                api.download_video(one_aid)
                self.linktext_signal.emit(api.getmsg('已完成: av{}'.format(one_aid.aid), "green"))

        self.progvalue_signal.emit(aid_count)

        f = float(time.time() - start)
        out_time = '%.2f' % f
        msg_d = "批量下载成功，耗时{}秒;\n所有视频保存在/Video文件夹中".format(out_time)
        self.linktext_signal.emit(api.getmsg(msg_d, "green"))
        try:
            api.open_explorer('\\Video')
        except:
            Exception()
            self.linktext_signal.emit(api.getmsg('打开文件夹失败, 请自行查看图像', "red"))

        self.status_signal.emit("当前状态：视频下载成功！")


class imgThread(QtCore.QThread):
    status_signal = QtCore.pyqtSignal(str)
    imgtext_signal = QtCore.pyqtSignal(str)
    progmax_signal = QtCore.pyqtSignal(int)
    progvalue_signal = QtCore.pyqtSignal(int)

    def __init__(self, aid_list):
        super().__init__()
        self.aid_list = aid_list[0]
        # self.imgfile = imgfile
        self.api = api.API()

    # @pysnooper.snoop()
    def invalid_input(self):
        self.status_signal.emit("当前状态：生成中...")
        self.imgtext_signal.emit(self.api.getmsg('输入不合法', "#464749"))

    # @pysnooper.snoop()
    def run(self):
        start = time.time()
        self.status_signal.emit("当前状态：生成中...")
        len_list = len(self.aid_list)
        self.progmax_signal.emit(len_list)
        msg_b = '获取av号总计{}个，开始批量生成图片...'.format(len_list)
        self.imgtext_signal.emit(self.api.getmsg(msg_b, "#464749"))
        for i in range(len_list):
            self.progvalue_signal.emit(i)
            one_aid = VideoPage(self.aid_list[i])
            self.imgtext_signal.emit(self.api.getmsg('生成弹幕分布...av{} {}'. \
                                                     format(one_aid.aid, one_aid.title), "#464749"))
            api.get_popularity(one_aid, False)
            self.imgtext_signal.emit(self.api.getmsg('已完成: av{}'.format(one_aid.aid), "green"))

        self.progvalue_signal.emit(len_list)

        f = float(time.time() - start)
        out_time = '%.2f' % f
        msg_d = "图片批量生成完毕，耗时{}秒;\n所有图片保存在/Graph文件夹中".format(out_time)
        self.imgtext_signal.emit(self.api.getmsg(msg_d, "green"))
        try:
            api.open_explorer('\\Graph')
        except:
            Exception()
            self.imgtext_signal.emit(self.api.getmsg('打开文件夹失败, 请自行查看图像', "red"))

        self.status_signal.emit("当前状态：图像输出完成！")


def main():
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    app = QtWidgets.QApplication(sys.argv)
    myui = MainUI()
    myui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
