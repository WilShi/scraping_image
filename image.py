# author: Wenbo Shi
#aim:爬取google图片

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import requests

# 使用代理的方法 ，可以直接windows使用代理，不用这么麻烦
# browserOptions = webdriver.ChromeOptions()
# browserOptions.add_argument('--proxy-server=ip:port)
# browser = webdriver.Chrome(chrome_options=browserOptions)

#修改keyword便可以修改搜索关键词
# keyword = '戴眼镜的人'
# url = 'https://www.google.com.hk/search?q='+keyword+'&tbm=isch'

url = 'https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1641819994082_R&pv=&ic=&nc=1&z=&hd=&latest=&copyright=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&dyTabStr=MCwzLDIsMSw0LDYsNSw3LDgsOQ%3D%3D&ie=utf-8&sid=&word=%E6%88%B4%E7%9C%BC%E7%94%B7%E4%BA%BA'


class Crawler_google_images:
    # 初始化
    def __init__(self):
        self.url = url

    # 获得Chrome驱动，并访问url
    def init_browser(self):
        # chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument("--disable-infobars")
        # browser = webdriver.Chrome(chrome_options=chrome_options)
        browser = webdriver.Chrome(ChromeDriverManager().install())
        # 访问url
        browser.get(self.url)
        # 最大化窗口，之后需要爬取窗口中所见的所有图片
        browser.maximize_window()
        return browser

    #下载图片
    def download_images(self, browser,round=2):
        picpath = './image'
        # 路径不存在时创建一个
        if not os.path.exists(picpath): os.makedirs(picpath)
        # 记录下载过的图片地址，避免重复下载
        img_url_dic = []

        count = 0 #图片序号
        pos = 0
        for i in range(round):
            pos += 500
            # 向下滑动
            js = 'var q=document.documentElement.scrollTop=' + str(pos)
            browser.execute_script(js)
            time.sleep(1)
            # 找到图片
            # html = browser.page_source#也可以抓取当前页面的html文本，然后用beautifulsoup来抓取
            #直接通过tag_name来抓取是最简单的，比较方便

            img_elements = browser.find_elements_by_tag_name('img')
            #遍历抓到的webElement
            for img_element in img_elements:
                img_url = img_element.get_attribute('src')
                # 前几个图片的url太长，不是图片的url，先过滤掉，爬后面的
                if isinstance(img_url, str):
                    if len(img_url) <= 200:
                        #将干扰的google图标筛去
                        if 'img' in img_url:
                            #判断是否已经爬过，因为每次爬取当前窗口，或许会重复
                            #实际上这里可以修改一下，将列表只存储上一次的url，这样可以节省开销，不过我懒得写了···
                            if img_url not in img_url_dic:
                                try:
                                    img_url_dic.append(img_url)
                                    #下载并保存图片到当前目录下
                                    filename = "./image/" + str(count) + ".jpg"
                                    r = requests.get(img_url)
                                    with open(filename, 'wb') as f:
                                        f.write(r.content)
                                    f.close()
                                    count += 1
                                    print('this is '+str(count)+'st img')
                                    #防止反爬机制
                                    time.sleep(0.2)
                                except:
                                    print('failure')

    def run(self):
        self.__init__()
        browser = self.init_browser()
        self.download_images(browser,20)#可以修改爬取的页面数，基本10页是100多张图片
        browser.close()
        print("爬取完成")


if __name__ == '__main__':
    craw = Crawler_google_images()
    craw.run()

    # print(url)

