import cv2
import mediapipe as mp
import time
import math

class poseDetector():
    
    def __init__(self, mode=False):
        self.mode = mode
    
        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode)

        
    def findPose(self, img, draw=True):
        
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
                
        return img
    
    def findPosition(self, img, draw=True):
        lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        return lmList
    
    def posture(self, img, draw=True):
        try:
            earx = self.results.pose_landmarks.landmark[self.mpPose.PoseLandmark.LEFT_EAR.value].x
            eary = self.results.pose_landmarks.landmark[self.mpPose.PoseLandmark.LEFT_EAR.value].y
            shoulderx = self.results.pose_landmarks.landmark[self.mpPose.PoseLandmark.LEFT_SHOULDER.value].x    
            shouldery = self.results.pose_landmarks.landmark[self.mpPose.PoseLandmark.LEFT_SHOULDER.value].y  
            
            difference = abs(earx-shoulderx)
            if difference == 0:
                posturePercent = 100
            else:
                posturePercent = (1-(difference/(math.sqrt(math.pow(abs(earx-shoulderx),2)+math.pow(abs(eary-shouldery),2)))))*100
            
            hipx = self.results.pose_landmarks.landmark[self.mpPose.PoseLandmark.LEFT_HIP.value].x
            hipy = self.results.pose_landmarks.landmark[self.mpPose.PoseLandmark.LEFT_HIP.value].y
            
            difference = abs(hipx-shoulderx)
            if difference == 0:
                posturePercent += 100
            else:
                posturePercent += (1-(difference/(math.sqrt(math.pow(abs(hipx-shoulderx),2)+math.pow(abs(hipy-shouldery),2)))))*100
            
            return posturePercent
        except:
            return 0
        
def main():
    cap = cv2.VideoCapture('videos/video1.mp4')
    pTime=0
    detector = poseDetector()
    while True:
        success, img = cap.read()
        img = detector.findPose(img)
        lmList = detector.findPosition(img)
    
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        
        cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 255, 0), 2)
        cv2.imshow("Video", img)
        if cv2.waitKey(1) == ord('q'):
            break
    
if __name__ == "__main__":
    main()