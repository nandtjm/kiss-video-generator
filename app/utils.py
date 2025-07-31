from PIL import Image
import cv2
import numpy as np

def validate_faces(img1_path, img2_path):
    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    return len(face_cascade.detectMultiScale(img1, 1.1, 4)) >= 1 and len(face_cascade.detectMultiScale(img2, 1.1, 4)) >= 1

def merge_side_by_side(img1_path, img2_path, size=(512,512)):
    from PIL import Image
    i1, i2 = Image.open(img1_path).convert('RGB'), Image.open(img2_path).convert('RGB')
    i1, i2 = i1.resize(size), i2.resize(size)
    canvas = Image.new('RGB',(size[0]*2, size[1]),(255,255,255))
    canvas.paste(i1,(0,0)); canvas.paste(i2,(size[0],0))
    return canvas
