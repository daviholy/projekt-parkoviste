import cv2
import os
import json
import argparse
from sys import exit
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument('--img_dir', type=str, default='./photos/',
                    help='directory where camera images should be stored')
parser.add_argument('-pp', '--parking_places', type=str, default='./parkingPlaces.json',
                    help='json file with parking places locations')
parser.add_argument('-cs', '--camera_source', default=0,
                    help='example: rtsp://username:password@192.168.1.64/1')
parser.add_argument('-img', '--src_img', type=str, default='./image4.png',
                    help='path to image that is used instead of camera input')


def load_json(file_path):

    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        exit("File " + file_path + " not found")


if __name__ == '__main__':
    args = parser.parse_args()

    # 1. Take a picture from camera
    cap = cv2.VideoCapture(args.camera_source)
    ret, frame = cap.read() if args.camera_source != 0 else (os.path.isfile(args.src_img), cv2.imread(args.src_img))
    if not ret:
        exit("Invalid camera/image source")
    cap.release()

    # 2. Load parking places locations
    parking_places = load_json(args.parking_places)

    # 3. Cut parking places and save them separately (in jpg 85% compression).
    i = 0
    for place, data in parking_places.items():
        x1, y1 = data['coordinates'][0]
        x2, y2 = data['coordinates'][1]
        i += 1
        img_name = "pl-" + str(i) + "-" + data['type'][0] + "_" + datetime.now().strftime("%y-%b-%d_%H-%M") + ".jpg"
        cv2.imwrite(args.img_dir+img_name, frame[y1:y2, x1:x2], [int(cv2.IMWRITE_JPEG_QUALITY), 85])