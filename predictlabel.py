import json

from PIL import Image

from yolo import YOLO

yolo = YOLO()

try:
    json_file = open('./class_indices.json', 'r')
    class_indict = json.load(json_file)
    print('class_indict:{}'.format(class_indict))
    print('class_indict:{}type'.format(type(class_indict)))
except Exception as e:
    print(e)
    exit(-1)


def predictsingle(image):
    try:
        r_image, resultList = yolo.detect_image(image, rate=0)
        print('resultList:{}'.format(resultList))
        r_image.show()
        global currentimg
        currentimg = r_image
        return resultList, r_image
    except:
        print('Open Error! Try again!')


def predictmulti(image):
    try:
        r_image, resultList = yolo.detect_image(image, rate=0)
        print('resultList:{}'.format(resultList))
        global currentimg
        currentimg = r_image
        return resultList, r_image
    except:
        print('Open Error! Try again!')
