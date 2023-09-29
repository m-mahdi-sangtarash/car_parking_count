import cv2 as cv
import pickle
import numpy as np

cap = cv.VideoCapture('vids_and_pics/carPark.mp4')

width = cap.get(cv.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv.CAP_PROP_FRAME_HEIGHT)
fps = cap.get(cv.CAP_PROP_FPS)
fourcc = cv.VideoWriter_fourcc(*"mp4v")
save_path = 'countParking-output.mp4'
vw = cv.VideoWriter(save_path, fourcc, int(fps), (int(width), int(height)), True)

with open('CarParkPos', 'rb') as f:
    posList = pickle.load(f)

width, height = 107, 48


def put_text_rect(img, text, pos, scale=3, thickness=1, colorT=(255, 255, 255), colorR=(255, 0, 255),
                  font=cv.FONT_HERSHEY_COMPLEX, offset=10, border=None, colorB=(0, 255, 0)):
    ox, oy = pos
    (w, h), _ = cv.getTextSize(text, font, scale, thickness)

    x1, y1, x2, y2 = ox - offset, oy - offset, ox + w + offset, oy - h - offset
    cv.rectangle(img, (x1, y1), (x2, y2), colorR, cv.FILLED)
    if border is not None:
        cv.rectangle(img, (x1, y1), (x2, y2), colorB, border)
    cv.putText(img, text, (ox, oy), font, scale, colorT, thickness)

    return img, [x1, y2, x2, y1]


def car_park_check(img):
    carpark_count = 0
    for pos in posList:
        x, y = pos
        carpark_img = img[y:y + height, x:x + width]
        whiteness = cv.countNonZero(carpark_img)

        if whiteness < 500:
            carpark_count += 1
            color = (0, 255, 0)
        else:
            color = (0, 0, 255)

        cv.rectangle(frame, pos, (pos[0] + width, pos[1] + height), color, 3)
        put_text_rect(frame, str(whiteness), (x, y + height), scale=0.5, thickness=1, offset=0, colorR=whiteness)

    put_text_rect(frame, f'Free: {carpark_count}/{len(posList)}', (50, 50), scale=1, thickness=1, offset=0,
                  colorR=(0, 200, 0))


while True:
    _, frame = cap.read()
    frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    imgBlur = cv.GaussianBlur(frame_gray, (3, 3), 1)
    imgThreshold = cv.adaptiveThreshold(imgBlur, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 25, 16)

    car_park_check(imgThreshold)
    cv.imshow('image', frame)
    vw.write(frame)
    if cv.waitKey(25) & 0xFF == ord('q'):
        break

cv.destroyAllWindows()
