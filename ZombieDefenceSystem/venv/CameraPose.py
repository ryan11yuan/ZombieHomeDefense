import cv2
import mediapipe as mp
import time
import PoseModule as pm
import win32com.client as comclt

cap = cv2.VideoCapture(0)
pTime=0
detector = pm.poseDetector()

sum=0
count=0
while True:
    success, img = cap.read()
    img = detector.findPose(img)
    #lmList = detector.findPosition(img)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    
    if detector.posture(img)==0:
        break
    else:
        sum+= detector.posture(img)
        count += 2
    
    cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 255, 0), 2)
    cv2.imshow("Video", img)
    if cv2.waitKey(1) == ord('q'):
        break
    
average = sum/count
print(average)
if average > 75:
    print("human")
else:
    wsh= comclt.Dispatch("WScript.Shell")
    wsh.AppActivate("sketch_may18a") 
    wsh.SendKeys("w")
    wsh.SendKeys("{ENTER}")
    print("zombie")

cap.release()
cv2.destroyAllWindows()