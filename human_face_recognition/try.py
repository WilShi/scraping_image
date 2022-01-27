import face_recognition
import cv2
import matplotlib.pyplot as plt
import sys
sys.path.append(r'C:/Users/cn-wilsonshi/Desktop/work/translation/transAPP')
from readfile import readfile

def find_face(img_path):

    image=face_recognition.load_image_file(img_path)
    face_locations=face_recognition.face_locations(image)

    face_num2=len(face_locations)
    print(face_num2)

    # if face_num2:
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
        cv2.imshow("Easmount-CSDN", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == "__main__":

    path = readfile().format_path(sys.argv[1])

    paths = readfile().listfiles(path)

    for i in paths:
        # i = i+'/'
        print(i)
        find_face(i)
