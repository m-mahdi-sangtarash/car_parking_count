import cv2 as cv
import pickle
import numpy as np

cap = cv.VideoCapture('vids_and_pics/carPark.mp4')

with open('CarParkPos', 'rb') as f:
    posList = pickle.load(f)

width, height = 107, 48


def car_park_check(img):
    carpark_count = 0
    for pos in posList:
        x, y = pos
        carpark_img = img[y, y + height, x, x + width]
        countfree = cv.countNonZero(carpark_img)

        if countfree < 900:
            carpark_count += 1


while True:
    _, frame = cap.read()
    frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    imgBlur = cv.GaussianBlur(frame, (3, 3), 1)
    imgThreshold = cv.adaptiveThreshold(imgBlur, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 25, 16)

    cv.imshow('image', frame)
    cv.imshow('imgThresh', imgBlur)

    if cv.waitKey(25) & 0xFF == ord('q'):
        break

cv.destroyAllWindows()
