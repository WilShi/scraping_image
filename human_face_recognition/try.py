import datetime
from itertools import count
import os
import time
import face_recognition
import cv2
import matplotlib.pyplot as plt
import sys
from PIL import Image, ImageDraw
from pathlib import Path
import random
from concurrent.futures import ThreadPoolExecutor
from pytube import YouTube
import numpy as np

from find_face import readfile

# face_recognition 文档：https://github.com/ageitgey/face_recognition/blob/master/README_Simplified_Chinese.md

def find_face(img_path, pass_dir, fail_dir):

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


# def find_faces(img_path, pass_dir, fail_dir):
#     print(img_path, "测试》》》》》")



def show_face_mark(path):
    image = face_recognition.load_image_file(path)

    #查找图像中所有面部的所有面部特征
    face_landmarks_list = face_recognition.face_landmarks(image)

    # print("I found {} face(s) in this photograph.".format(len(face_landmarks_list)))

    if not face_landmarks_list:
        print("无法识别到人脸！！！！")
        return False

    tmp = None
    for face_landmarks in face_landmarks_list:

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
        pil_image = Image.fromarray(image) if not tmp else tmp
        d = ImageDraw.Draw(pil_image)

        for facial_feature in facial_features:
            d.line(face_landmarks[facial_feature], width=1)
        tmp = pil_image
    pil_image.show()


def load_video(path):
    start = datetime.datetime.now()

    input_video = cv2.VideoCapture(path)

    length = int(input_video.get(cv2.CAP_PROP_FRAME_COUNT))
    print("帧数: ", length)

    # 创建输出视频文件（确保输出视频文件的分辨率/帧速率与输入视频匹配）
    fourcc = cv2.VideoWriter_fourcc(*'XVID')

    #可以右键查看所读取的视频文件的帧速、率帧高度、帧宽度
    output_video = cv2.VideoWriter('Obama.avi', fourcc, 25, (640, 360))


    for i in range(length):
        ret, image = input_video.read()

        face_landmarks_list = face_recognition.face_landmarks(image)

        if face_landmarks_list:
            tmp = None
            for face_landmarks in face_landmarks_list:

                #打印此图像中每个面部特征的位置
                facial_features = [
                    'left_eyebrow',
                    'right_eyebrow',
                    'chin',
                    'nose_bridge',
                    'nose_tip',
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
                pil_image = Image.fromarray(image) if not tmp else tmp
                d = ImageDraw.Draw(pil_image)

                for facial_feature in facial_features:
                    d.line(face_landmarks[facial_feature], width=1)
                tmp = pil_image

                # pil_image.show()
            image_arr = np.array(pil_image)
            output_video.write(image_arr)

        else:
            print("No face found")
            print("**"*40)
            output_video.write(image)

        t = int((datetime.datetime.now() - start).seconds)
        if t >= 1:
            print(f"{i}/{length} {'='*10} 每秒：{round(i/t)} 张")
        
    output_video.release()

    end = datetime.datetime.now()
    print(f"总图片：{length} 张 {'*'*10} 用时：{(end - start).seconds} 秒 {'*'*10} 每秒：{round(length/int((end - start).seconds))} 张")


video = []
def count_unit(img):
    # print(f"这个图片的大小是{len(img)}")
    face_landmarks_list = face_recognition.face_landmarks(img)

    if face_landmarks_list: 
        print("Yes")
        video.append("1")
    else: 
        print("No")
        video.append("0")


def testfast(path):
    start = datetime.datetime.now()

    input_video = cv2.VideoCapture(path)

    length = int(input_video.get(cv2.CAP_PROP_FRAME_COUNT))
    print("帧数: ", length)

    video_list = []
    for i in range(length):
        ret, image = input_video.read()
        video_list.append(image)

    pool = ThreadPoolExecutor(max_workers=2)
    for i in video_list:
        pool.submit(count_unit, i)
    pool.shutdown()


if __name__ == "__main__":

    # pool = ThreadPoolExecutor(max_workers=2)

    # path = readfile().format_path(sys.argv[1])
    # paths = readfile().listfiles(path)

    # fail_dir = '{}/Downloads/finish_fail/'.format(str(Path.home()))
    # pass_dir = '{}/Downloads/finish_pass/'.format(str(Path.home()))


    # start = datetime.datetime.now()

    # for i in paths:
    #     # print(i)
    #     if ".jpg" in i:
    #         find_face(i, pass_dir, fail_dir)

    # #         pool.submit(find_face, i, pass_dir, fail_dir)

    # # pool.shutdown()

    # end = datetime.datetime.now()
    # print(f"总用时：{(end - start).seconds} 秒")


    # path = readfile().format_path(sys.argv[1])
    # show_face_mark(path)

    load_video(r"C:\\Users\\cn-wilsonshi\\Downloads\\Obama.mp4")

    # testfast(r"C:\\Users\\cn-wilsonshi\\Downloads\\videoplayback.mp4")
