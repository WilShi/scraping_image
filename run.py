import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from Ui_appView import Ui_Form
from image import Crawler_google_images

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
        self.textBrowser.setText("开始从链接：{}\n获取图片".format(url))
        path = self.craw.run(url, page, filename)
        self.textBrowser.setText("图片爬取结束！！！！\n文件保存在{}".format(path))


    def google(self):
        url = self.search_lineEdit.text()
        page = self.page_lineEdit.text()
        url = 'https://www.google.com.hk/search?q={}&tbm=isch'.format(url)
        print(url)
        self.craw.run(url, page, url)


    def baidu(self):
        url = self.search_lineEdit.text()
        page = self.page_lineEdit.text()
        wurl = 'https://image.baidu.com/search/index?tn=baiduimage&word={}'.format(url)
        print(url)
        self.craw.run(wurl, page, url)

    def zip_(self):
        url = self.search_lineEdit.text()
        self.craw.zipf(url)

    
    def count(self):
        url = self.search_lineEdit.text()
        count = self.craw.countfile(url)
        print("文件夹内有：{} 个文件".format(str(count)))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyMainForm()
    myWin.show()
    sys.exit(app.exec_())