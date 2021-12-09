from HandTrackingModule import HandDetector
from Keyboard import Keyboard, Key
from GestureSaver import GestureSaver

from traceback import format_exc
import cv2
import time


class ImageReader:
    def __init__(self, display_fps=True) -> None:
        self._pTime = 0 #previous
        self._cTime = 0 #current
        self._display_fps = display_fps
        self._cap = cv2.VideoCapture(0)

    def loop_until(self, condition=True):
        if isinstance(condition, bool):
            condition = lambda: condition
        if not callable(condition):
            raise ValueError(f"{format_exc} condition variable have to be bool type or callable.")
        while condition():
            succes, img = self._cap.read()
            yield img

    @staticmethod
    def get_mirror_view(img):
        return cv2.flip(img, 1)
            
    def display_fps(self, img):
        if self._display_fps:
            fps = self._calculate_fps()
            cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN,2, (255,255,255),3) #10,70 to pozycja tekstu, 2 to skala, (255,0,255) to kolor, 3 to grubość 
        return img

    def _calculate_fps(self) -> int:
        self._cTime = time.time()
        fps = 1/(self._cTime-self._pTime)
        self._pTime = self._cTime
        return fps

    @staticmethod
    def display_image(img):
        cv2.imshow("Image", img)
        cv2.waitKey(1)

def main():
    hand_detector = HandDetector()
    pTime = 0 #previous
    cTime = 0 #current
    cap = cv2.VideoCapture(0)


    with open("gesture_saves.txt", "a") as file:

        gesture_saver = GestureSaver(file, "OpenedHand", 100)

        ######### konfiguracja klawiatury #########
        keyboard = Keyboard()
        a_key = Key()
        a_key.name = "a"
        a_key.set_function_on_press(gesture_saver.start_recoding)
        s_key = Key()
        s_key.name ="s"
        s_key.set_function_on_press(gesture_saver.end_recording)
        keyboard.add_keys((a_key,s_key))
        ###########################################


        while not gesture_saver.all_images_are_captured():    
            succes, img = cap.read()
            
            hands_landmarks = hand_detector.find_hands(img)
            
            cTime = time.time()
            fps = 1/(cTime-pTime)
            pTime = cTime

            img = cv2.flip(img, 1)

            cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN,3, (255,0,255),3) #10,70 to pozycja tekstu, 2 to skala, (255,0,255) to kolor, 3 to grubość 
            if gesture_saver.is_recording:
                cv2.putText(img, "Recording...", (10,105), cv2.FONT_HERSHEY_PLAIN,2, (255,0,255),2) #10,70 to pozycja tekstu, 2 to skala, (255,0,255) to kolor, 3 to grubość 
                gesture_saver.capture_hand_landmarks(hands_landmarks)
            cv2.imshow("Image", img)
            cv2.waitKey(1)


if __name__=="__main__":
    main()


    