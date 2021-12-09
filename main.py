from HandTrackingModule import HandDetector
from Keyboard import Keyboard, Key
import cv2
import time





def main():
    hand_detector = HandDetector()
    pTime = 0 #previous
    cTime = 0 #current
    cap = cv2.VideoCapture(0)


    ######### rzeczy do pliku ########
    class Flag:
        def __init__(self) -> None:
            self._status = False
        
        @property
        def status(self) -> bool:
            return self._status
        
        def rise(self):
            self._status = True

        def drop(self):
            self._status = False

    recording_flag = Flag()
    gesture_name = "OpenHand"
    captured_count = 0
    need_to_capture = 100
    ##################################

    ######### konfiguracja klawiatury #########
    keyboard = Keyboard()
    a_key = Key()
    a_key.name = "a"
    a_key.set_function_on_press(recording_flag.rise)
    s_key = Key()
    s_key.name ="s"
    s_key.set_function_on_press(recording_flag.drop)
    keyboard.add_keys((a_key,s_key))
    ###########################################

    with open("gesture_saves.txt", "a") as file:
        while True:    
            succes, img = cap.read()
            
            hands_landmarks = hand_detector.find_hands(img)
            
            cTime = time.time()
            fps = 1/(cTime-pTime)
            pTime = cTime

            img = cv2.flip(img, 1)

            cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN,3, (255,0,255),3) #10,70 to pozycja tekstu, 2 to skala, (255,0,255) to kolor, 3 to grubość 
            if recording_flag.status:
                cv2.putText(img, "Recording...", (10,105), cv2.FONT_HERSHEY_PLAIN,2, (255,0,255),2) #10,70 to pozycja tekstu, 2 to skala, (255,0,255) to kolor, 3 to grubość 
                if hands_landmarks:
                    file.write(f"{gesture_name}|")
                    hands_landmark_strings = [f"{x},{y}" for x, y in hands_landmarks[0]]
                    file.write(";".join(hands_landmark_strings))  
                    file.write("\n")                     
                    captured_count += 1
            if captured_count == need_to_capture:
                return
            if captured_count > need_to_capture:
                raise ValueError("Too many gestures were captured.")
            cv2.imshow("Image", img)
            cv2.waitKey(1)


if __name__=="__main__":
    main()


    