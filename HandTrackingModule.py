import cv2
import mediapipe as mp
import time
import numpy as np

class HandDetector():
    def __init__(self, 
                static_image_mode = False,
                max_num_hands = 2,
                min_detection_confidence = 0.5,
                #min_tracking_confidence = 0.5
            ) -> None:
        
        self.mode = static_image_mode
        self.maxHands = max_num_hands
        self.detectionCon = min_detection_confidence
        #self.trackCon = min_tracking_confidence
                
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode, 
            max_num_hands=self.maxHands, 
            min_detection_confidence=self.detectionCon
        ) #, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils


    def find_hands(self, img, draw=True):
        self.imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_height, img_width, channel = img.shape #height, width, channel
        processed_image = self.hands.process(self.imgRGB)
        hands_list = []
        if processed_image.multi_hand_landmarks:
            for hand_landmarks in processed_image.multi_hand_landmarks:   #handLms to landmarki dla jednej ręki wykrytej 
                if draw:
                    self.mpDraw.draw_landmarks(img, hand_landmarks, self.mpHands.HAND_CONNECTIONS)
                
                landmarks_list = np.empty(shape=(21,2), dtype=np.int16)
                for id, landmark in enumerate(hand_landmarks.landmark): 
                    x, y = (int(landmark.x*img_width), int(landmark.y*img_height))
                    landmarks_list[id][0] = x
                    landmarks_list[id][1] = y
                
                hands_list.append(landmarks_list)
        return hands_list


def main():
    hand_detector = HandDetector()
    pTime = 0 #previous
    cTime = 0 #current
    cap = cv2.VideoCapture(0)

    while True:    
        succes, img = cap.read()
        

        print(hand_detector.find_hands(img))
        
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime


        cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN,3, (255,0,255),3) #10,70 to pozycja tekstu, 2 to skala, (255,0,255) to kolor, 3 to grubość 


        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()