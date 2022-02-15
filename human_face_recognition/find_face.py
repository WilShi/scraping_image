#coding:utf-8
import datetime
from itertools import count
import os
import re
import time
import face_recognition
import cv2
import matplotlib.pyplot as plt
import sys
from PIL import Image, ImageDraw
from pathlib import Path
import random
import dlib
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Process

import numpy as np

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



# face_recognition 文档：https://github.com/ageitgey/face_recognition/blob/master/README_Simplified_Chinese.md

def find_face_cv2(img_path):

    # 读取原始图像
    img = cv2.imread(img_path)

    # 调用熟悉的人脸分类器 检测特征类型
    # 人脸 - haarcascade_frontalface_default.xml
    # 人眼 - haarcascade_eye.xm
    # 微笑 - haarcascade_smile.xml
    face_detect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    # 检查人脸 按照1.1倍放到 周围最小像素为5
    face_zone = face_detect.detectMultiScale(img, scaleFactor=1.1, minNeighbors=5)
    print ('识别人脸的信息：',face_zone)

    if face_zone != ():

        # 绘制矩形和圆形检测人脸
        for x, y, w, h in face_zone:
            # 绘制矩形人脸区域 thickness表示线的粗细
            cv2.rectangle(img, pt1=(x, y), pt2=(x+w, y+h),color=[0,0,255], thickness=2)
            # 绘制圆形人脸区域 radius表示半径
            cv2.circle(img, center=(x+w//2, y+h//2), radius=w//2, color=[0,255,0], thickness=2)

        # 设置图片可以手动调节大小
        cv2.namedWindow("Easmount-CSDN", 0)

        # 显示图片
        cv2.imshow("Easmount-CSDN", img)

        # 等待显示 设置任意键退出程序
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def find_face_fr(img_path, pass_dir, fail_dir):

    image=face_recognition.load_image_file(img_path)

    face_locations=face_recognition.face_locations(image)

    face_num2=len(face_locations)
    # print(face_num2)

    if face_num2:
        print(f"{img_path} {'='*10} pass")
        return True
        
        if not os.path.exists(pass_dir): os.makedirs(pass_dir)
        Image.open(img_path).convert('RGB').save(f"{pass_dir}{random.randint(1, 10000000000)}.jpg")

        # org=cv2.imread(img_path)
        # for i in range(0,face_num2):
        #     top=face_locations[i][0]
        #     right=face_locations[i][1]
        #     bottom=face_locations[i][2]
        #     left=face_locations[i][3]
            
        #     start=(left,top)
        #     end=(right,bottom)
            
        #     color=(0,255,0)
        #     thickness=5
        #     img=cv2.rectangle(org,start,end,color,thickness)
            
        # plt.imshow(img)
        # plt.axis("off")
        # plt.show()

    if face_num2 == 0:
        print(f"{img_path} {'='*10} fail")
        return False
        
        if not os.path.exists(fail_dir): os.makedirs(fail_dir)
        Image.open(img_path).convert('RGB').save(f"{fail_dir}{random.randint(1, 10000000000)}.jpg")

        # cv2.imshow("Easmount-CSDN", image)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()


def mkdir(path):
    path = re.findall("(.*/)", path)[0]
    print("当前路径：", path)
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)
        print("#"*50)
        print("建立新的文件路径于: {}".format(path))
        print("#"*50)


def writeFile(path, file):
    mkdir(path)
    with open(path, 'w', encoding='UTF-8') as f:
        f.write(file)
    f.close
    print("成功写入文件至: {}".format(path))
    return path


def mark_face_detail(path):

    try:
        image = face_recognition.load_image_file(path)
        #查找图像中所有面部的所有面部特征
        face_landmarks_list = face_recognition.face_landmarks(image)
        face_landmarks = face_landmarks_list[0]
    except Exception as error:
        print("无法识别到人脸！！！！")
        return False


    allx = 0
    ally = 0
    for i in face_landmarks['right_eye']:
        allx += i[0]
        ally += i[1]

    lex = round(allx/len(face_landmarks['right_eye']))
    ley = round(ally/len(face_landmarks['right_eye']))

    # print("left eye:", lex, ley, '\n', "**"*40)

    allx = 0
    ally = 0
    for i in face_landmarks['left_eye']:
        allx += i[0]
        ally += i[1]

    rex = round(allx/len(face_landmarks['right_eye']))
    rey = round(ally/len(face_landmarks['right_eye']))

    # print("right eye:", rex, rey, '\n', "**"*40)

    nsx = face_landmarks['nose_bridge'][-1][0]
    nsy = face_landmarks['nose_bridge'][-1][1]

    # print("nose:", nsx, nsy, '\n', "**"*40)

    maxt = max(face_landmarks['top_lip'])
    maxb = max(face_landmarks['bottom_lip'])
    lm = maxt if maxt == maxb else max([maxt, maxb])
    lmx = lm[0]
    lmy = lm[1]

    # print("left lip:", lmx, lmy, '\n', "**"*40)

    mint = min(face_landmarks['top_lip'])
    minb = min(face_landmarks['bottom_lip'])
    rm = mint if mint == minb else min([mint, minb])
    rmx = rm[0]
    rmy = rm[1]

    # print("right lip:", rmx, rmy, '\n', "**"*40)


    ffpfile = f"LEX {lex}\nLEY {ley}\nREX {rex}\nREY {rey}\nNSX {nsx}\nNSY {nsy}\nLMX {lmx}\nLMY {lmy}\nRMX {rmx}\nRMY {rmy}"

    # print(ffpfile)

    filename = readfile().last_path(path)
    filename = filename.replace('jpg', 'ffp')

    dir = '{}/Downloads/FFP/{}'.format(str(Path.home()), filename)

    writeFile(dir, ffpfile)


def show_face_mark(path):
    image = face_recognition.load_image_file(path)

    #查找图像中所有面部的所有面部特征
    face_landmarks_list = face_recognition.face_landmarks(image)

    # print("I found {} face(s) in this photograph.".format(len(face_landmarks_list)))

    if not face_landmarks_list:
        print("无法识别到人脸！！！！")
        return False

    face_landmarks = face_landmarks_list[0]

    #打印此图像中每个面部特征的位置
    facial_features = [
        'chin',
        'nose_bridge',
        'left_eye',
        'right_eye',
        'top_lip',
        'bottom_lip'
    ]

    for facial_feature in facial_features:
        print("The {} in this face has the following points: {}".format(facial_feature, face_landmarks[facial_feature]))
    
    # 获取面部标记点
    print("**"*40)

    # 在图像中描绘出每个人脸特征！
    pil_image = Image.fromarray(image)
    d = ImageDraw.Draw(pil_image)

    for facial_feature in facial_features:
        d.line(face_landmarks[facial_feature], width=1)
    pil_image.show()



def unit_mark_face_detail(paths):
    for path in paths:
        mark_face_detail(path)


def multprocess(paths):
    start = datetime.datetime.now()

    length = len(paths)
    p1 = []
    p2 = []
    p3 = []
    p4 = []
    p5 = []

    for i in range(length):
        if i < round(length/5):
            p1.append(paths[i])
        elif i >= round(length/5) and i <(2*round(length/5)):
            p2.append(paths[i])
        elif i >= (2*round(length/5)) and i < (3*round(length/5)):
            p3.append(paths[i])
        elif i >= (3*round(length/5)) and i < (4*round(length/5)):
            p4.append(paths[i])
        else:
            p5.append(paths[i])

    multp = [p1,p2,p3,p4,p5]
    
    # q = Queue()
    process_list = []
    for i in multp:
        print("开始运行")
        p = Process(target=unit_mark_face_detail,args=(i,))
        p.start()
        process_list.append(p)

    for p in process_list:
        p.join()


    end = datetime.datetime.now()
    print(f"总图片：{length} 张 {'*'*10} 用时：{(end - start).seconds} 秒 {'*'*10} 每秒：{round(length/int((end - start).seconds))} 张")



def start(path):

    path = readfile().format_path(path)
    paths = readfile().listfiles(path)

    fail_dir = '{}/Downloads/finish_fail/'.format(str(Path.home()))
    pass_dir = '{}/Downloads/finish_pass/'.format(str(Path.home()))


    start = datetime.datetime.now()

    tmp_pass = []
    tmp_fail = []
    for i in paths:
        # print(i)
        if ".jpg" in i:
            if find_face_fr(i, pass_dir, fail_dir):
                tmp_pass.append(i)
            else:
                tmp_fail.append(i)

    tmp_pass2 = []
    for i in tmp_pass:
        # print(i)
        if ".jpg" in i:
            if find_face_fr(i, pass_dir, fail_dir):
                tmp_pass2.append(i)
            else:
                tmp_fail.append(i)

    tmp_pass3 = []
    for i in tmp_pass2:
        # print(i)
        if ".jpg" in i:
            if find_face_fr(i, pass_dir, fail_dir):
                tmp_pass3.append(i)
            else:
                tmp_fail.append(i)

    tmp_pass4 = []
    for i in tmp_pass3:
        # print(i)
        if ".jpg" in i:
            if find_face_fr(i, pass_dir, fail_dir):
                tmp_pass4.append(i)
            else:
                tmp_fail.append(i)

    
    for i in tmp_pass4:
        if not os.path.exists(pass_dir): os.makedirs(pass_dir)
        Image.open(i).convert('RGB').save(f"{pass_dir}{random.randint(1, 10000000000)}.jpg")


    for i in tmp_fail:
        if not os.path.exists(fail_dir): os.makedirs(fail_dir)
        Image.open(i).convert('RGB').save(f"{fail_dir}{random.randint(1, 10000000000)}.jpg")


    end = datetime.datetime.now()
    print(f"总图片：{len(paths)} 张 {'*'*10} 用时：{(end - start).seconds} 秒 \
        \n通过了 {len(tmp_pass4)} 张图片 {'*'*10} 否定了 {len(tmp_fail)} 张图片 \
        \n通过率 {round(len(tmp_pass4)/len(paths)*100, 2)}%")


def test(path):

    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    detector = dlib.get_frontal_face_detector()
    rects = detector(gray, 0)
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
    dets = detector(img, 1)

    for k, d in enumerate(dets):
        print("dets{}".format(d))
        print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
            k, d.left(), d.top(), d.right(), d.bottom()))
    
        # 使用predictor进行人脸关键点识别 shape为返回的结果
        shape = predictor(img, d)


        # # 获取第一个和第二个点的坐标（相对于图片而不是框出来的人脸）
        # print("Part 0: {}, Part 1: {} ...".format(shape.part(0), shape.part(1)))
    
        # # 绘制特征点
        # for index, pt in enumerate(shape.parts()):
        #     print('Part {}: {}'.format(index, pt))
        #     pt_pos = (pt.x, pt.y)
        #     cv2.circle(img, pt_pos, 1, (255, 0, 0), 2)
        #     #利用cv2.putText输出1-68
        #     font = cv2.FONT_HERSHEY_SIMPLEX
        #     cv2.putText(img, str(index+1),pt_pos,font, 0.3, (0, 0, 255), 1, cv2.LINE_AA)

        def shape_to_np(dlib_shape, dtype="int"):
            # 初始化 (x, y) 坐标列表
            coordinates = np.zeros((dlib_shape.num_parts, 2), dtype=dtype)
            # 循环所有面部特征点，并将其转换为 (x, y) 坐标的元组
            for i in range(0, dlib_shape.num_parts):
                coordinates[i] = (dlib_shape.part(i).x, dlib_shape.part(i).y)
            # 返回 (x,y) 坐标的列表
            return coordinates

        # 定义不同特征点取值切片
        JAWLINE_POINTS = list(range(0, 17))
        RIGHT_EYEBROW_POINTS = list(range(17, 22))
        LEFT_EYEBROW_POINTS = list(range(22, 27))
        NOSE_BRIDGE_POINTS = list(range(27, 31))
        LOWER_NOSE_POINTS = list(range(31, 36))
        RIGHT_EYE_POINTS = list(range(36, 42))
        LEFT_EYE_POINTS = list(range(42, 48))
        MOUTH_OUTLINE_POINTS = list(range(48, 61))
        MOUTH_INNER_POINTS = list(range(61, 68))
        ALL_POINTS = list(range(0, 68))
        # 使用线条绘制面部特征点
        def draw_shape_lines_all(np_shape, image):
            draw_shape_lines_range(np_shape, image, JAWLINE_POINTS)
            draw_shape_lines_range(np_shape, image, RIGHT_EYEBROW_POINTS)
            draw_shape_lines_range(np_shape, image, LEFT_EYEBROW_POINTS)
            draw_shape_lines_range(np_shape, image, NOSE_BRIDGE_POINTS)
            draw_shape_lines_range(np_shape, image, LOWER_NOSE_POINTS)
            draw_shape_lines_range(np_shape, image, RIGHT_EYE_POINTS, True)
            draw_shape_lines_range(np_shape, image, LEFT_EYE_POINTS, True)
            draw_shape_lines_range(np_shape, image, MOUTH_OUTLINE_POINTS, True)
            draw_shape_lines_range(np_shape, image, MOUTH_INNER_POINTS, True)

        # 连接不同的点来绘制曲线形状
        def draw_shape_lines_range(np_shape, image, range_points, is_closed=False):
            np_shape_display = np_shape[range_points]
            points = np.array(np_shape_display, dtype=np.int32)
            cv2.polylines(image, [points], is_closed, (255, 255, 0), thickness=2, lineType=cv2.LINE_8)

        # 函数调用
        draw_shape_lines_all(shape_to_np(shape), img)
 
    cv2.imshow('img', img)
    k = cv2.waitKey()
    cv2.destroyAllWindows()



if __name__ == "__main__":

    if sys.argv[1] == 'face':
        start(sys.argv[2])

    if sys.argv[1] == 'mark':
        path = readfile().format_path(sys.argv[2])
        paths = readfile().listfiles(path)

        start = datetime.datetime.now()
        notfind = []
        for i in paths:
            # print(i)
            if mark_face_detail(i) == False:
                notfind.append(i)

        print(f"{len(notfind)} 张图片无法找到，需人工检查！！！！")
        for i in notfind:
            print(i)

        end = datetime.datetime.now()
        print(f"总图片：{len(paths)} 张 {'*'*10} 用时：{(end - start).seconds} 秒 {'*'*10} 每秒：{round(len(paths)/int((end - start).seconds))} 张")


    if sys.argv[1] == 'show':
        path = readfile().format_path(sys.argv[2])
        show_face_mark(path)

    if sys.argv[1] == 'mult':
        path = readfile().format_path(sys.argv[2])
        paths = readfile().listfiles(path)

        multprocess(paths)

    if sys.argv[1] == 'test':
        # pool = ThreadPoolExecutor(max_workers=2)

        # path = readfile().format_path(sys.argv[2])
        # paths = readfile().listfiles(path)

        # for i in paths:
        #     t = pool.submit(mark_face_detail, i)
        #     # if not t.running():
        #     #     time.sleep(5)
        #     # print(i)

        # pool.shutdown()

        test(sys.argv[2])

    # face_detail(r"C:/Users/cn-wilsonshi/Downloads/old_version/glasses/20.jpg")

    

