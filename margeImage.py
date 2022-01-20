import os
from sys import argv
from PIL import Image

def Picture_Synthesis(mother_img, son_img, save_img, coordinate=None):
    """
    :param mother_img: 母图
    :param son_img: 子图
    :param save_img: 保存图片名
    :param coordinate: 子图在母图的坐标
    :return:
    """
    #将图片赋值,方便后面的代码调用
    M_Img = Image.open(mother_img)
    S_Img = Image.open(son_img)
    factor = 1#子图缩小的倍数1代表不变，2就代表原来的一半

    #给图片指定色彩显示格式
    M_Img = M_Img.convert("RGB")  # CMYK/RGBA 转换颜色格式（CMYK用于打印机的色彩，RGBA用于显示器的色彩）

    # 获取图片的尺寸
    M_Img_w, M_Img_h = M_Img.size  # 获取被放图片的大小（母图）
    print("母图尺寸：",M_Img.size)

    S_Img_w, S_Img_h = S_Img.size  # 获取小图的大小（子图）
    print("子图尺寸：",S_Img.size)

    size_w = int(S_Img_w / factor)
    size_h = int(S_Img_h / factor)

    # 防止子图尺寸大于母图
    if S_Img_w > size_w:
        S_Img_w = size_w
    if S_Img_h > size_h:
        S_Img_h = size_h

    # # 重新设置子图的尺寸
    # icon = S_Img.resize((S_Img_w, S_Img_h), Image.ANTIALIAS)
    icon = S_Img.resize((S_Img_w, S_Img_h), Image.ANTIALIAS)
    w = int((M_Img_w - S_Img_w) / 2)
    h = int((M_Img_h - S_Img_h) / 2)

    try:
        if coordinate==None or coordinate=="":
            coordinate=(w, h)
            # 粘贴子图到母图的指定坐标（当前居中）
            M_Img.paste(icon, coordinate, mask=None)
        else:
            print("已经指定坐标")
            # 粘贴子图到母图的指定坐标（当前居中）
            M_Img.paste(icon, coordinate, mask=None)
    except:
        print("坐标指定出错 ")
    # 保存图片
    M_Img.save(save_img)


class readfile():

    def __init__(self) -> None:
        self.files = []

    def allfile(self, path) -> None:
        if os.path.isdir(path):
            files = os.listdir(path)
            for file in files:
                new_file = path+'/'+file
                if os.path.isdir(new_file):
                    self.allfile(new_file)
                else:
                    self.files.append(new_file)
        else:
            self.files.append(path)

    def listfiles(self, path) -> list:
        path = self.format_path(path)
        self.allfile(path)
        return self.files

    def format_path(self, path) -> str:
        path = os.path.abspath(path)
        path = path.replace('\\', '/')
        path = path.replace('//', '/')
        path = path[:-1] if path[-1] == '/' else path
        return path

    def last_path(self, path) -> str:
        path = path[path.rfind('/')+1:]
        return path

    def sub_path(self, path, rootpath) -> str:
        path = path[path.find(rootpath)+len(rootpath):]
        path = path[1:] if path[0] == '/' else path
        return path


if __name__ == "__main__":

    # Picture_Synthesis(mother_img=argv[1], son_img=argv[2], save_img=argv[3], coordinate=(300, 280))

    files = readfile().listfiles(argv[1])

    for img in files:
        print(img)
        print(readfile().last_path(img))

        sip = readfile().format_path(r"C:\Users\cn-wilsonshi\Downloads\shiwenbo\shiwenbo\墨渍\1.jpeg")
        svip = readfile().format_path(r"C:\Users\cn-wilsonshi\Desktop\work\scraping_image\marge_image/"+readfile().last_path(img))
        Picture_Synthesis(img, sip, svip, coordinate=(330, 200))

        sip = readfile().format_path(r"C:\Users\cn-wilsonshi\Downloads\shiwenbo\shiwenbo\墨渍\11.jpeg")
        svip = readfile().format_path(r"C:\Users\cn-wilsonshi\Desktop\work\scraping_image\marge_image/"+readfile().last_path(img))
        Picture_Synthesis(svip, sip, svip, coordinate=(310, 0))
