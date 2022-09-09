import cv2 
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.8)
colorR = (255, 0, 255)

# original center (cx, cy) & height/width (w,h) of the rectangle, 
# will be changed later the drag&drop
cx, cy, w, h = 100, 100, 200, 200

class DragRect():
    def __init__(self, posCenter, size=[200, 200]):
        self.posCenter = posCenter 
        self.size = size 
    def update(self, cursor):
        cx, cy = self.posCenter 
        w, h = self.size 

        # check if the finger is in the rect
        if cx-w//2 < cursor[0] < cx+w//2 and cy-h//2 < cursor[1] < cy+h//2:
            self.posCenter = cursor

rectList = []
for x in range(5):
    rectList.append(DragRect([x*250+150, 150]))

while True:
    seccess, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    
    lmList, _ = detector.findPosition(img)

    # if there's hand exits in camera
    if lmList:

        # 8,12 are the number of fingertips, l is the dist between the two
        l, _, _ = detector.findDistance(8,12,img,draw=False)

        if l<50:
            cursor = lmList[0]
            # call the update 
            for rect in rectList:
                rect.update(cursor)

    # Draw
    for rect in rectList:
        cx, cy = rect.posCenter
        w, h = rect.size
        cv2.rectangle(img, (cx-w//2, cy-h//2), (cx+w//2, cy+h//2), colorR, cv2.FILLED)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
    