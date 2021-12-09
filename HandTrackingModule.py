import mediapipe as mp
import numpy as np
import cv2


class HandDetector():
    def __init__(self, 
                static_image_mode = False,
                max_num_hands = 1,
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




if __name__ == "__main__":
    pass
