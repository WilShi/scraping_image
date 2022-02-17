from base64 import decode
import datetime
from itertools import count
import json
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
from multiprocessing import Process, Queue
import pickle

from sqlalchemy import true

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
    output_video = cv2.VideoWriter('ttttt.avi', fourcc, 25, (640, 360))


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


# # 测试多线程
# def count_unit(lis):
#     # print(f"这个图片的大小是{len(img)}")

#     ans = []
#     for i in range(len(lis)):
#         img = lis[i]
#         face_landmarks_list = face_recognition.face_landmarks(img)

#         if face_landmarks_list: 
#             print("Yes")
#             ans.append("1")
#         else: 
#             print("No")
#             ans.append("0")
#     return ans


# def testfast(path):
#     start = datetime.datetime.now()

#     input_video = cv2.VideoCapture(path)

#     length = int(input_video.get(cv2.CAP_PROP_FRAME_COUNT))
#     print("帧数: ", length)

#     video_list = []
#     for i in range(length):
#         ret, image = input_video.read()
#         video_list.append(image)

#     p1v = video_list[:20]
#     p2v = video_list[20:41]
#     multp = [p1v, p2v]

#     res = []
#     pool = ThreadPoolExecutor(max_workers=2)
#     for i in multp:
#         res.append(pool.submit(count_unit, i))
#     for i in res:
#         print(i.result())

#     pool.shutdown()



# 测试多进程
def unit_mark(dic):
    start = datetime.datetime.now()

    key = list(dic)[0]
    lis = dic[key]

    # 创建输出视频文件（确保输出视频文件的分辨率/帧速率与输入视频匹配）
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    #可以右键查看所读取的视频文件的帧速、率帧高度、帧宽度
    output_video = cv2.VideoWriter(f'{key}.avi', fourcc, 25, (640, 360))

    for i in range(len(lis)):
        img = lis[i]
        face_landmarks_list = face_recognition.face_landmarks(img)

        print(f"{i+1}/{len(lis)}")

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

                # for facial_feature in facial_features:
                #     print("The {} in this face has the following points: {}".format(facial_feature, face_landmarks[facial_feature]))
                
                # # 获取面部标记点
                # print("**"*40)

                # 在图像中描绘出每个人脸特征！
                pil_image = Image.fromarray(img) if not tmp else tmp
                d = ImageDraw.Draw(pil_image)

                for facial_feature in facial_features:
                    d.line(face_landmarks[facial_feature], width=1)
                tmp = pil_image

                # pil_image.show()
            image_arr = np.array(pil_image)
            output_video.write(image_arr)

        else: output_video.write(img)

        t = int((datetime.datetime.now() - start).seconds)
        if t >= 1:
            print(f"{i}/{len(lis)} {'='*10} 每秒：{round(i/t)} 张")

    output_video.release()


    # out = {key:l}
    # q.put(out)


def prework(path):
    start = datetime.datetime.now()

    input_video = cv2.VideoCapture(path)
    length = int(input_video.get(cv2.CAP_PROP_FRAME_COUNT))
    print("帧数: ", length)
    video_list = []
    p1v = []
    p2v = []
    for i in range(length):
        ret, image = input_video.read()
        # video_list.append(image)
        if i <= length//2:
            p1v.append(image)
        else:
            p2v.append(image)
    
    # p1v = video_list[:20]
    # p2v = video_list[20:41]
    multp = [{'1':p1v}, {'2':p2v}]

    f = open('prework.pickle', 'wb')
    pickle.dump(multp, f)
    f.close

    end = datetime.datetime.now()
    print(f"预处理视频用时：{(end - start).seconds} 秒")


def deletefile(path):
    while True:
        try:
            os.remove(path)
            print(f"删除文件：{path}")
            break
        except Exception as error:
            print("等待解除权限......")
            time.sleep(2)


def marge_video(multp):
    # 创建输出视频文件（确保输出视频文件的分辨率/帧速率与输入视频匹配）
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    #可以右键查看所读取的视频文件的帧速、率帧高度、帧宽度
    output_video = cv2.VideoWriter('test_marge.avi', fourcc, 25, (640, 360))

    for i in multp:
        part_video = cv2.VideoCapture(f"{list(i)[0]}.avi")
        length = int(part_video.get(cv2.CAP_PROP_FRAME_COUNT))
        for j in range(length):
            ret, image = part_video.read()
            output_video.write(image)

    output_video.release()


def testfast(path):

    start = datetime.datetime.now()

    input_video = cv2.VideoCapture(path)
    length = int(input_video.get(cv2.CAP_PROP_FRAME_COUNT))

    # length = 500

    print("帧数: ", length)
    p1v = []
    p2v = []
    p3v = []
    p4v = []

    for i in range(length):
        ret, image = input_video.read()
        if i < round(length/4):
            p1v.append(image)
        elif i >= round(length/4) and i <(2*round(length/4)):
            p2v.append(image)
        elif i >= (2*round(length/4)) and i < (3*round(length/4)):
            p3v.append(image)
        else:
            p4v.append(image)

    multp = [{'1':p1v}, {'2':p2v}, {'3':p3v}, {'4':p4v}]
    
    # q = Queue()
    process_list = []
    for i in multp:
        print("开始运行")
        p = Process(target=unit_mark,args=(i,))
        p.start()
        process_list.append(p)

    for p in process_list:
        p.join()


    end = datetime.datetime.now()
    print(f"总图片：{length} 张 {'*'*10} 用时：{(end - start).seconds} 秒 {'*'*10} 每秒：{round(length/int((end - start).seconds))} 张")


    print("开始导出视频......")
    start = datetime.datetime.now()

    
    p = Process(target=marge_video, args=(multp,))
    p.start()
    p.join()
    

    process_list = []
    for i in multp:
        path = f"{list(i)[0]}.avi"
        p = Process(target=deletefile, args=(path,))
        p.start()
        process_list.append(p)
    
    for p in process_list:
        p.join()

    end = datetime.datetime.now()
    print(f"导出视频用时：{(end - start).seconds} 秒")



def bin_image(path):

    SCALE = 0.3
    #等比例缩放

    def get_char(pixel, blank_char='0', fill_char='1'):
        print(pixel)

        if pixel == 0:
            return blank_char
        else:
            return fill_char



    im = Image.open(path)
    size = im.size
    #获取图片的像素
    #size[0]*size[1] 横宽像素
    width, height = int(size[0] * SCALE), int(size[1] * SCALE)
    im = im.resize((width, height))#修改图片尺寸
    im = im.convert('2')#获得二值图像

    im.show()

    txt = ""
    for i in range(height):
        for j in range(width):
            txt += get_char(im.getpixel((j, i)))#getpixel是获取图像中某一点像素的RGB颜色值
        txt += '\n'
    #print(txt)
    # f = open(r'gou.txt', 'w')

    print(txt)

    # f.close()



if __name__ == "__main__":
    start = datetime.datetime.now()

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

    # load_video(r"C:\\Users\\cn-wilsonshi\\Downloads\\videoplayback.mp4")

    # testfast(r"C:\\Users\\cn-wilsonshi\\Downloads\\guanvideo.mp4")

    bin_image(r"C:\\Users\\cn-wilsonshi\\Downloads\\finish\\111\\153065424.jpg")

    # prework("C:\\Users\\cn-wilsonshi\\Downloads\\videoplayback.mp4")

    
    

    # f = open('prework.pickle', 'rb')
    # load_file = pickle.load(f)

    # print(len(load_file[0]['1']))
    # print(len(load_file[1]['2']))


    # # 创建输出视频文件（确保输出视频文件的分辨率/帧速率与输入视频匹配）
    # fourcc = cv2.VideoWriter_fourcc(*'XVID')
    # #可以右键查看所读取的视频文件的帧速、率帧高度、帧宽度
    # output_video = cv2.VideoWriter('1111111111.avi', fourcc, 25, (640, 360))

    # for i in range(len(load_file)):
    #     for img in load_file[i][str(i+1)]:
    #         # img = np.array(img)
    #         # print(img)
    #         output_video.write(img)

    # output_video.release()




    # a = [1,2,3,4,5,6,7,8,9,10,11,12]

    # p1v=[]
    # p2v=[]
    # p3v=[]
    # p4v=[]

    # for i in range(len(a)):
    #     if i < round(len(a)/4):
    #         p1v.append(a[i])
    #     elif i >= round(len(a)/4) and i < (2*round(len(a)/4)):
    #         p2v.append(a[i])
    #     elif i >= (2*round(len(a)/4)) and i < (3*round(len(a)/4)):
    #         p3v.append(a[i])
    #     else:
    #         p4v.append(a[i])

    # print(a)
    # print(p1v)
    # print(p2v)
    # print(p3v)
    # print(p4v)



    # # 创建输出视频文件（确保输出视频文件的分辨率/帧速率与输入视频匹配）
    # fourcc = cv2.VideoWriter_fourcc(*'XVID')
    # #可以右键查看所读取的视频文件的帧速、率帧高度、帧宽度
    # output_video = cv2.VideoWriter('test_marge.avi', fourcc, 25, (640, 360))

    # for i in [{'1':1}, {'2':1}, {'3':1}, {'4':1}]:
    #     name = list(i)[0]
    #     part_video = cv2.VideoCapture(f"{name}.avi")
    #     length = int(part_video.get(cv2.CAP_PROP_FRAME_COUNT))
    #     for j in range(length):
    #         ret, image = part_video.read()
    #         output_video.write(image)
        
    # output_video.release()

    end = datetime.datetime.now()
    print(f"程序总用时：{(end - start).seconds} 秒")
