#coding:utf-8
import datetime
from itertools import count
import os
import time
import face_recognition
import cv2
import matplotlib.pyplot as plt
import sys
from PIL import Image
from pathlib import Path
import random
import dlib
from concurrent.futures import ThreadPoolExecutor

sys.path.append(r'C:/Users/cn-wilsonshi/Desktop/work/translation/transAPP')
from readfile import readfile

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

    if face_zone == ():

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
        
        if not os.path.exists(pass_dir): os.makedirs(pass_dir)
        Image.open(img_path).convert('RGB').save(f"{pass_dir}{random.randint(1, 10000000000)}.jpg")

    #     org=cv2.imread(img_path)
    #     for i in range(0,face_num2):
    #         top=face_locations[i][0]
    #         right=face_locations[i][1]
    #         bottom=face_locations[i][2]
    #         left=face_locations[i][3]
            
    #         start=(left,top)
    #         end=(right,bottom)
            
    #         color=(0,255,0)
    #         thickness=5
    #         img=cv2.rectangle(org,start,end,color,thickness)
            
    #     plt.imshow(img)
    #     plt.axis("off")
    #     plt.show()

    if face_num2 == 0:
        print(f"{img_path} {'='*10} fail")

        
        if not os.path.exists(fail_dir): os.makedirs(fail_dir)
        Image.open(img_path).convert('RGB').save(f"{fail_dir}{random.randint(1, 10000000000)}.jpg")

        # cv2.imshow("Easmount-CSDN", image)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()


def face_detail(path):
    img=cv2.imread(path)
    gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    detector=dlib.get_frontal_face_detector()
    predictor=dlib.shape_predictor(r"C:\ProgramData\Anaconda3\Lib\site-packages\face_recognition_models\models\shape_predictor_68_face_landmarks.dat")
    #predictor=dlib.shape_predictor(r"C:\ProgramData\Anaconda3\Lib\site-packages\face_recognition_models\models\shape_predictor_5_face_landmarks.dat")

    dets=detector(gray, 1)
    for face in dets:
        shape=predictor(img,face)
        for pt in shape.parts():
            pt_pos=(pt.x,pt.y)
            img=cv2.circle(img,pt_pos,2,(0,255,0),5)
            
    plt.imshow(img)
    plt.axis('off')
    plt.show()


def start(path):

    path = readfile().format_path(path)
    paths = readfile().listfiles(path)

    fail_dir = '{}/Downloads/finish_fail/'.format(str(Path.home()))
    pass_dir = '{}/Downloads/finish_pass/'.format(str(Path.home()))


    start = datetime.datetime.now()

    for i in paths:
        # print(i)
        if ".jpg" in i:
            find_face_fr(i, pass_dir, fail_dir)

    end = datetime.datetime.now()
    print(f"总图片：{len(paths)} 张 {'*'*10} 用时：{(end - start).seconds} 秒")


if __name__ == "__main__":

    # start(sys.argv[1])
    face_detail(r"C:/Users/cn-wilsonshi/Downloads/old_version/glasses/11.jpg")
