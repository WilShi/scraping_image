import random
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from Ui_appView import Ui_Form
from image import Crawler_google_images
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

class MyMainForm(QMainWindow, Ui_Form):

    def __init__(self, parent=None) -> None:
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)
        self.craw = Crawler_google_images()

        self.link_pushButton.clicked.connect(self.link)
        self.google_pushButton.clicked.connect(self.google)
        self.baidu_pushButton.clicked.connect(self.baidu)
        self.zip_pushButton.clicked.connect(self.zip_)
        self.count_pushButton.clicked.connect(self.count)


    def link(self):
        
        url = self.search_lineEdit.text()
        page = self.page_lineEdit.text()
        filename = self.filename_lineEdit.text() if self.filename_lineEdit.text() else 'image'
        self.textBrowser.setText("开始从链接：{}\n\n获取图片".format(url))
        QApplication.processEvents()
        path = self.run(url, page, filename)
        # self.textBrowser.setText("图片爬取结束！！！！\n\n文件保存在:\n\n{}".format(path))


    def google(self):
        
        url = self.search_lineEdit.text()
        page = self.page_lineEdit.text()
        self.textBrowser.setText("开始从谷歌图片寻找 {} 图片".format(url))
        QApplication.processEvents()
        wurl = 'https://www.google.com.hk/search?q={}&tbm=isch'.format(url)
        print(url)
        path = self.run(wurl, page, url)
        # self.textBrowser.setText("图片爬取结束！！！！\n\n文件保存在:\n\n{}".format(path))


    def baidu(self):
        
        url = self.search_lineEdit.text()
        page = self.page_lineEdit.text()
        self.textBrowser.setText("开始从百度图片寻找 {} 图片".format(url))
        QApplication.processEvents()
        wurl = 'https://image.baidu.com/search/index?tn=baiduimage&word={}'.format(url)
        print(url)
        path = self.run(wurl, page, url)
        # self.textBrowser.setText("图片爬取结束！！！！\n\n文件保存在:\n\n{}".format(path))


    def zip_(self):
        url = self.search_lineEdit.text()
        zippath = self.craw.zipf(url)
        self.textBrowser.setText("压缩文件成功！！！！\n\n文件保存在{}".format(zippath))

    
    def count(self):
        url = self.search_lineEdit.text()
        count = self.craw.countfile(url)
        print("文件夹内有：{} 个文件".format(str(count)))
        self.textBrowser.setText("{} 文件夹拥有 {} 个文件".format(url, count))


    def run(self, url, page=20, dir='image'):
        dir = '{}/Downloads/finish/{}'.format(str(Path.home()), dir)

        self.textBrowser.setText("请等待......\n\n正在初始化可监控浏览器窗口......\n\n".format(url))
        QApplication.processEvents()
        browser = self.craw.init_browser(url)

        self.textBrowser.setText("请等待......\n\n正在通过：\n\n {} \n\n链接寻找图片......\n\n".format(url))
        QApplication.processEvents()
        url_list = self.craw.download_images(browser, url, int(page), dir)#可以修改爬取的页面数，基本10页是100多张图片
        browser.close()

        listlen = len(url_list)
        self.textBrowser.setText("获取到了 {} 张图片\n\n开始下载图片......\n\n\n由于是多线程下载所以无法显示进度！！！！".format(str(listlen)))
        QApplication.processEvents()

        pool = ThreadPoolExecutor(max_workers=10)
        count = 1
        for image_url in url_list:
            # msg = self.craw.download_url(url, image_url, dir, count)

            pool.submit(self.craw.download_url, url, image_url, dir, random.randint(1, 10000000000))

            # self.textBrowser.setText("获取到了 {} 张图片\n\n\n{}\n\n\n下载进度：{}/{} （{}%）\n\n\n{}"\
            #     .format(str(listlen), msg, str(count), str(listlen), str(round(count/listlen*100, 2)), self.process_bar(int(count/listlen*100), 100)))
            # QApplication.processEvents()
            # count += 1

        pool.shutdown()


        print('#'*50)
        print("爬取和打包文件完成！！！！")
        print("文件路径为：{}".format(self.craw.format_path(dir)))
        print('#'*50)

        self.textBrowser.setText("图片爬取结束！！！！\n\n文件保存在:\n\n{}\n\n本文件没有压缩，如需压缩可以将文件路径复制进‘链接/关键词’的输入框然后点击压缩按钮......".format(self.craw.format_path(dir)))
        QApplication.processEvents()

        return self.craw.format_path(dir)


    def process_bar(self, num, total):
        rate = float(num)/total
        barnum = int(20*rate)
        r = '[{}{}]'.format('*'*barnum,'_'*(20-barnum))
        return r
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyMainForm()
    myWin.show()
    sys.exit(app.exec_())