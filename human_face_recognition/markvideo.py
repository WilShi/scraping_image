#! -*- coding: utf-8 -*-

from base64 import decode
import datetime
import os
import time
import face_recognition
import cv2
import sys
from PIL import Image, ImageDraw
import numpy as np
from multiprocessing import Process, Queue

from find_face import readfile


class MarkVideo:

    def __init__(self, rate, width, hight) -> None:
        self.rate = rate
        self.width = width
        self.hight = hight


    def load_video(self, path, output_name):
        start = datetime.datetime.now()

        input_video = cv2.VideoCapture(path)

        length = int(input_video.get(cv2.CAP_PROP_FRAME_COUNT))
        print("帧数: ", length)

        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        output_video = cv2.VideoWriter(f'{output_name}', fourcc, self.rate, (self.width, self.hight))


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

                    # 在图像中描绘出每个人脸特征！
                    pil_image = Image.fromarray(image) if not tmp else tmp
                    d = ImageDraw.Draw(pil_image)

                    for facial_feature in facial_features:
                        d.line(face_landmarks[facial_feature], width=1)
                    tmp = pil_image

                image_arr = np.array(pil_image)
                output_video.write(image_arr)

            else:
                output_video.write(image)

            t = int((datetime.datetime.now() - start).seconds)
            if t >= 1:
                print(f"{i}/{length} 已用时：{t} 秒 {'='*10} 每秒：{round(i/t)} 张")
            
        output_video.release()

        end = datetime.datetime.now()
        print(f"总图片：{length} 张 {'*'*10} 用时：{(end - start).seconds} 秒 {'*'*10} 每秒：{round(length/int((end - start).seconds))} 张")


    def marge_video(self, multp, output_name):
        # 创建输出视频文件（确保输出视频文件的分辨率/帧速率与输入视频匹配）
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        #可以右键查看所读取的视频文件的帧速、率帧高度、帧宽度
        output_video = cv2.VideoWriter(f'{output_name}', fourcc, self.rate, (self.width, self.hight))

        for i in multp:
            part_video = cv2.VideoCapture(i)
            length = int(part_video.get(cv2.CAP_PROP_FRAME_COUNT))
            for j in range(length):
                ret, image = part_video.read()
                output_video.write(image)

        output_video.release()


    def deletefile(self, path):
        while True:
            try:
                os.remove(path)
                print(f"删除文件：{path}")
                break
            except Exception as error:
                print("等待解除权限......")
                time.sleep(2)


    def prework(self, input_video, length):
        """
        Cut video to 5 small video part,
        return each video part name.
        """
        start = datetime.datetime.now()

        print("视频总帧数: ", length)

        fourcc = cv2.VideoWriter_fourcc(*'XVID')

        part1 = cv2.VideoWriter('1.avi', fourcc, self.rate, (self.width, self.hight))
        part2 = cv2.VideoWriter('2.avi', fourcc, self.rate, (self.width, self.hight))
        part3 = cv2.VideoWriter('3.avi', fourcc, self.rate, (self.width, self.hight))
        part4 = cv2.VideoWriter('4.avi', fourcc, self.rate, (self.width, self.hight))
        part5 = cv2.VideoWriter('5.avi', fourcc, self.rate, (self.width, self.hight))

        for i in range(length):
            ret, image = input_video.read()
            if i < round(length/5):
                part1.write(image)

            elif i >= round(length/5) and i <(2*round(length/5)):
                part2.write(image)

            elif i >= (2*round(length/5)) and i < (3*round(length/5)):
                part3.write(image)

            elif i >= (3*round(length/5)) and i < (4*round(length/5)):
                part4.write(image)

            else:
                part5.write(image)

        part1.release()
        part2.release()
        part3.release()
        part4.release()
        part5.release()

        end = datetime.datetime.now()
        print(f"导出视频用时：{(end - start).seconds} 秒")

        return ['1.avi', '2.avi', '3.avi', '4.avi', '5.avi']


    def multprocess(self, path, output_name):

        start = datetime.datetime.now()

        output_name += '.avi' if '.avi' not in output_name else output_name

        input_video = cv2.VideoCapture(path)
        length = int(input_video.get(cv2.CAP_PROP_FRAME_COUNT))

        length = 1000

        partvideos = self.prework(input_video, length)
        spt = []

        process_list = []
        for i in partvideos:
            print("开始运行")
            opfn = f'1{i}'
            spt.append(opfn)
            p = Process(target=self.load_video,args=(i,opfn,))
            p.start()
            process_list.append(p)

        for p in process_list:
            p.join()


        end = datetime.datetime.now()
        print(f"总图片：{length} 张 {'*'*10} 用时：{(end - start).seconds} 秒 {'*'*10} 每秒：{round(length/int((end - start).seconds))} 张")


        print("开始导出视频......")
        start = datetime.datetime.now()

        p = Process(target=self.marge_video, args=(spt,output_name,))
        p.start()
        p.join()
        
        partvideos += spt
        process_list = []
        for path in partvideos:
            p = Process(target=self.deletefile, args=(path,))
            p.start()
            process_list.append(p)
        
        for p in process_list:
            p.join()

        end = datetime.datetime.now()
        print(f"导出视频用时：{(end - start).seconds} 秒")


if __name__ == "__main__":

    MarkVideo(24, 1280, 720).multprocess(r"C:\\Users\\cn-wilsonshi\\Downloads\\ted.mp4", "ted")