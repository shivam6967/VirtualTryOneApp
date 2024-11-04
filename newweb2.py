import os
import cvzone
import cv2
from cvzone.PoseModule import PoseDetector

cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Set the width of the frame
cap.set(4, 720)  # Set the height of the frame

detector = PoseDetector()

shirtsFolderPath = "Resources/Shirts"
listShirts = os.listdir(shirtsFolderPath)

fixedRatio = 262 / 190
shirtRatioHeightWidth = 581 / 440
imageNumber = 0
imgButtonRight = cv2.imread("Resources/button.png", cv2.IMREAD_UNCHANGED)
imgButtonLeft = cv2.flip(imgButtonRight, 1)
counterRight = 0
counterLeft = 0
selectionSpeed = 10

while True:
    success, img = cap.read()
    img = detector.findPose(img)

    lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False, draw=False)

    if lmList:
        indexed_lmList = []

        for index, lm in enumerate(lmList):
            indexed_lmList.append([index] + lm)

        lm11 = indexed_lmList[11][1:3]
        lm12 = indexed_lmList[12][1:3]

        imgShirt = cv2.imread(os.path.join(shirtsFolderPath, listShirts[imageNumber]), cv2.IMREAD_UNCHANGED)
        widthofShirt = int((lm11[0] - lm12[0]) * fixedRatio)
        imgShirt = cv2.resize(imgShirt, (widthofShirt, int(widthofShirt * shirtRatioHeightWidth)))
        currentScale = (lm11[0] - lm12[0]) / 190
        offset = int(44 * currentScale), int(48 * currentScale)

        try:
            img = cvzone.overlayPNG(img, imgShirt, (lm12[0] - offset[0], lm12[1] - offset[1]))
        except:
            pass

        img = cvzone.overlayPNG(img, imgButtonRight, (1074, 293))
        img = cvzone.overlayPNG(img, imgButtonLeft, (72, 293))

        if indexed_lmList[16][1] < 300:
            counterRight += 1
            cv2.ellipse(img, (139, 360), (66, 66), 0, 0, counterRight * selectionSpeed, (0, 255, 0), 20)
            if counterRight * selectionSpeed > 360:
                counterRight = 0
                if imageNumber < len(listShirts) - 1:
                    imageNumber += 1
        elif indexed_lmList[15][1] > 900:
            counterLeft += 1
            cv2.ellipse(img, (1138, 360), (66, 66), 0, 0, counterLeft * selectionSpeed, (0, 255, 0), 20)
            if counterLeft * selectionSpeed > 360:
                counterLeft = 0
                if imageNumber > 0:
                    imageNumber -= 1
        else:
            counterRight = 0
            counterLeft = 0

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
