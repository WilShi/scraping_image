# coding: utf-8
# author: Wenbo Shi
#aim:爬取google图片

import random
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from pathlib import Path
import time
import os
import requests
import sys
import zipfile
import base64, re
from concurrent.futures import ThreadPoolExecutor


class Crawler_google_images:
    # 初始化
    def __init__(self):
        self.proxy = '127.0.0.1:41091'
        self.proxies = {
            'http': 'http://' + self.proxy,
            'https': 'https://' + self.proxy
        }

    # 获得Chrome驱动，并访问url
    def init_browser(self, url):
        # chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument("--disable-infobars")
        # browser = webdriver.Chrome(chrome_options=chrome_options)
        option=webdriver.ChromeOptions()
        option.add_argument('headless')

        browser = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=option)
        # 访问url
        browser.get(url)
        # 最大化窗口，之后需要爬取窗口中所见的所有图片
        browser.maximize_window()
        return browser


    def download_images(self, browser, url, round=2, picpath='image'):

        # picpath = './finish/{}'.format(picpath)
        # 路径不存在时创建一个
        if not os.path.exists(picpath): os.makedirs(picpath)
        # 记录下载过的图片地址，避免重复下载
        img_url_dic = []

        
        pos = 0
        for i in range(round):
            print("目前正在获取第 {} 页的图片......".format(str(i+1)))
            pos += 500
            # 向下滑动
            js = 'var q=document.documentElement.scrollTop=' + str(pos)
            browser.execute_script(js)
            
            try:
                show_more_button = browser.find_element(By.CSS_SELECTOR, "input[value='顯示更多結果']")
                if show_more_button.is_displayed():
                    show_more_button.click()
                    print("自动点击'加载更多'按钮......")
                    time.sleep(2)
            except Exception as error:
                try:
                    show_more_button = browser.find_element(By.CSS_SELECTOR, "input[value='显示更多搜索结果']")
                    if show_more_button.is_displayed():
                        show_more_button.click()
                        print("自动点击'加载更多'按钮......")
                        time.sleep(2)
                except Exception as error:
                    pass

                pass
            time.sleep(0.5)
        # 找到图片
        # html = browser.page_source#也可以抓取当前页面的html文本，然后用beautifulsoup来抓取
        #直接通过tag_name来抓取是最简单的，比较方便

        img_elements = browser.find_elements_by_tag_name('img')
        #遍历抓到的webElement
        for img_element in img_elements:
            img_url = img_element.get_attribute('src')
            # 前几个图片的url太长，不是图片的url，先过滤掉，爬后面的
            if isinstance(img_url, str):
                if len(img_url) <= 200 or "http" in img_url:
                    #将干扰的google图标筛去
                    if 'img' in img_url or 'image' in img_url:
                        #判断是否已经爬过，因为每次爬取当前窗口，或许会重复
                        #实际上这里可以修改一下，将列表只存储上一次的url，这样可以节省开销，不过我懒得写了···
                        if img_url not in img_url_dic:
                            img_url_dic.append(img_url)

                else:
                    img_url = img_url[img_url.find(',')+1:]

                    if img_url not in img_url_dic:
                        img_url_dic.append(img_url)

        print("获取到了 {} 张图片".format(str(len(img_url_dic))))
        return img_url_dic

                        
    def download_url(self, url, img_url, picpath, count):

        filename = "{}/{}.jpg".format(picpath, str(count))
        filename = self.format_path(filename)

        if len(img_url) <= 200 or "http" in img_url:
            try:
                if 'google' in url:
                    r = requests.get(img_url, proxies=self.proxies)
                else:
                    r = requests.get(img_url)
                with open(filename, 'wb') as f:
                    f.write(r.content)
                f.close()
                print('this is {}.jpg st img this image is from a url'.format(str(count)))
                # time.sleep(0.2)
                return "成功通过URL链接下载 {}.jpg 图片".format(str(count))
            except:
                print('failure')
                return False
        else:
            r = base64.b64decode(img_url)
            with open(filename, 'wb') as f:
                f.write(r)
            f.close()
            # count += 1
            print('this is {}.jpg st img this image is from base64 encode'.format(str(count)))
            # time.sleep(0.2)
            return "成功通过base64获取 {}.jpg 图片".format(str(count))


    def run(self, url, page=20, dir='image'):
        dir = '{}/Downloads/finish/{}'.format(str(Path.home()), dir)
        self.__init__()
        browser = self.init_browser(url)
        url_list = self.download_images(browser, url, int(page), dir)#可以修改爬取的页面数，基本10页是100多张图片
        browser.close()

        pool = ThreadPoolExecutor(max_workers=10)

        for image_url in url_list:
            pool.submit(self.download_url, url, image_url, dir, random.randint(1, 10000000000))
        pool.shutdown()

        self.zipf(dir)
        print('#'*50)
        print("爬取和打包文件完成！！！！")
        print("文件路径为：{}".format(dir))
        print('#'*50)
        return self.format_path(dir)


    def format_path(self, path) -> str:
        path = os.path.abspath(path)
        path = path.replace('\\', '/')
        path = path.replace('//', '/')
        path = path[:-1] if path[-1] == '/' else path
        return path


    # 压缩文件夹
    def zipf(self, dir):
        dir = dir.replace('\\', '/')
        dir = dir[:-1] if dir[-1] == '/' else dir
        # dir = dir[dir.rfind('/')+1:] if '/' in dir else dir
        # print(dir)
        zippath = '{}.zip'.format(dir)
        zippath = self.format_path(zippath)

        zip = zipfile.ZipFile(zippath, 'w', zipfile.ZIP_DEFLATED)
        for path, dirnames, filenames in os.walk('{}'.format(dir)):
            fpath = path.replace('{}'.format(dir), '')
            for filename in filenames:
                zip.write(os.path.join(path, filename), os.path.join(fpath, filename))
        # zip.write('./{}'.format(dir))
        zip.close()
        print("压缩文件成功！！！！\n文件保存在{}".format(zippath))
        return zippath


    def countfile(self, path):
        path = path.replace('\\', '/')
        count = 0
        if os.path.isdir(path):
            files = os.listdir(path)
            for file in files:
                new_file = path + '/' + file
                if os.path.isdir(new_file):
                    count += self.countfile(new_file)
                else:
                    count+=1
        return count


if __name__ == '__main__':

    craw = Crawler_google_images()

    if len(sys.argv) > 2:
        if sys.argv[1] == "link" or sys.argv[1] == "url":
            craw.run(sys.argv[2], sys.argv[3], sys.argv[4])
        elif sys.argv[1] == "zip":
            craw.zipf(sys.argv[2])
        elif sys.argv[1] == "count":
            count = craw.countfile(sys.argv[2])
            print("文件夹内有：{} 个文件".format(str(count)))
        elif sys.argv[1] == "google":
            url = 'https://www.google.com.hk/search?q={}&tbm=isch'.format(sys.argv[2])
            print(url)
            craw.run(url, sys.argv[3], sys.argv[2])
        elif sys.argv[1] == "baidu":
            url = 'https://image.baidu.com/search/index?tn=baiduimage&word={}'.format(sys.argv[2])
            print(url)
            craw.run(url, sys.argv[3], sys.argv[2])
        else:
            print("{error: 1, msg: python image.py [link|url, zip, count, google, baidu] [pages, dirName, dirName, keyword, keyword] [dirName, '', '', pages, pages]}")
    else:
        print("{error: 1, msg: python image.py [link|url, zip, count, google, baidu] [pages, dirName, dirName, keyword, keyword] [dirName, '', '', pages, pages]}")


