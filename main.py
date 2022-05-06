import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

#importing all images
image_background = cv2.imread("D:\pythonProject\Pong Game\Resources\Background.png")
img_game_over = cv2.imread("D:\pythonProject\Pong Game\Resources\gameOver.png")
img_ball = cv2.imread("D:\pythonProject\Pong Game\Resources\Ball.png", cv2.IMREAD_UNCHANGED)
bat1 = cv2.imread(r"D:\pythonProject\Pong Game\Resources\bat1.png", cv2.IMREAD_UNCHANGED)
bat2 = cv2.imread(r"D:\pythonProject\Pong Game\Resources\bat2.png", cv2.IMREAD_UNCHANGED)

#hand detector
detector = HandDetector(detectionCon=0.8, maxHands=2)

#variables
ball_pos = [100,100]
speedX = 15
speedY = 15
gameOver = False
score = [0,0]

while True:
    _, img = cap.read()
    #find hand and its landmark
    hands, img = detector.findHands(img, flipType=False) #draw= False
    imgRaw = img.copy()

    # overlaying the background image
    img = cv2.addWeighted(img, 0.2, image_background, 0.8, 0)

    #check for the hand
    if hands:
        for hand in hands:
            x,y,w,h = hand['bbox']
            h1, w1, _ = bat1.shape
            y1 = y - h1//2
            y1 = np.clip(y1,20,415)

            if hand['type'] == 'Left':
                img = cvzone.overlayPNG(img, bat1, (59,y1))
                if 59 < ball_pos[0] < 59 + w1 and y1 < ball_pos[1] <y1 + h1:
                    speedX = -speedX-5
                    ball_pos[0] += 30
                    score[0] +=1


            if hand['type'] == 'Right':
                img = cvzone.overlayPNG(img, bat2, (1195, y1))
                if 1195-50 < ball_pos[0] < 1195-30 + w1 and y1 < ball_pos[1] <y1 + h1:
                    speedX = -speedX-5
                    ball_pos[0] -= 30
                    score[1] += 1


    #game over
    if ball_pos[0] <40 or ball_pos[0]>1200:
        gameOver= True

    if gameOver:
        img = img_game_over
        cv2.putText(img, str(score[1]*2).zfill(2), (585, 360), cv2.FONT_HERSHEY_COMPLEX,
                   2.5, (200, 0, 200), 5)

    #if game not over move the ball
    else:

        #move the ball
        if ball_pos[1]>= 500 or ball_pos[1]<=10:
            speedY = -speedY

        ball_pos[0] += speedX
        ball_pos[1] += speedY

        #draw the ball
        img =cvzone.overlayPNG(img,img_ball,ball_pos)

        cv2.putText(img, str(score[0]), (300,650), cv2.FONT_HERSHEY_COMPLEX,3, (255,255,255), 5)
        cv2.putText(img, str(score[1]), (900, 650), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 5)

    img[580:700,20:233] = cv2.resize(imgRaw,(213,120))

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key ==ord('r'):
        ball_pos = [100, 100]
        speedX = 12
        speedY = 12
        gameOver = False
        score = [0, 0]
        img_game_over = cv2.imread("D:\pythonProject\Pong Game\Resources\gameOver.png")

    elif key==ord('e'):
        gameOver =True


