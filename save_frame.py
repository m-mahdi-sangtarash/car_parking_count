import cv2 as cv


cap = cv.VideoCapture('vids_and_pics/carPark.mp4')

_, frame = cap.read()
cv.imwrite('vids_and_pics/carParkmg.png', frame)