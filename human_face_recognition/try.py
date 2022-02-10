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
from concurrent.futures import ThreadPoolExecutor
from pytube import YouTube

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





if __name__ == "__main__":

    pool = ThreadPoolExecutor(max_workers=2)

    path = readfile().format_path(sys.argv[1])
    paths = readfile().listfiles(path)

    fail_dir = '{}/Downloads/finish_fail/'.format(str(Path.home()))
    pass_dir = '{}/Downloads/finish_pass/'.format(str(Path.home()))


    start = datetime.datetime.now()

    for i in paths:
        # print(i)
        if ".jpg" in i:
            find_face(i, pass_dir, fail_dir)

    #         pool.submit(find_face, i, pass_dir, fail_dir)

    # pool.shutdown()

    end = datetime.datetime.now()
    print(f"总用时：{(end - start).seconds} 秒")
