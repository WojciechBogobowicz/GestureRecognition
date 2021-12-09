from traceback import format_exc
import cv2
import time


class CameraReader:
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
        while not condition():
            succes, img = self._cap.read()
            yield img

    @staticmethod
    def get_mirror_view(img):
        return cv2.flip(img, 1)

    @staticmethod
    def add_label(img, message):
        return cv2.putText(img, message, (10,105), cv2.FONT_HERSHEY_PLAIN,2, (0,0,0),2) #10,70 to pozycja tekstu, 2 to skala, (255,0,255) to kolor, 3 to grubość 

    def display_fps(self, img):
        if self._display_fps:
            fps = self._calculate_fps()
            cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN,2, (0,0,0),3) #10,70 to pozycja tekstu, 2 to skala, (255,0,255) to kolor, 3 to grubość 
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
