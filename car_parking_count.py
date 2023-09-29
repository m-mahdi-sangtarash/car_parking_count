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
        carpark_img = img[y:y + height, x:x + width]
        whiteness = cv.countNonZero(carpark_img)

        def put_text_rect():
            pass

        if whiteness < 900:
            carpark_count += 1
            color = (0, 255, 0)
        else:
            color = (0, 0, 255)

        cv.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, 3)
        put_text_rect(img, str(whiteness), (x, y + height), scale=1, thickness=2, offset=0, colorR=whiteness)

    put_text_rect(img, f'Free: {carpark_count}/{len(posList)}', (100, 50), scale=3, thickness=5, offset=20,
                  colorR=(0, 200, 0))


while True:
    _, frame = cap.read()
    frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    imgBlur = cv.GaussianBlur(frame_gray, (3, 3), 1)
    imgThreshold = cv.adaptiveThreshold(imgBlur, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 25, 16)
    car_park_check(imgThreshold)
    cv.imshow('image', frame)

    if cv.waitKey(25) & 0xFF == ord('q'):
        break

cv.destroyAllWindows()
