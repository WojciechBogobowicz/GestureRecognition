from traceback import format_exc


class GestureSaver:
    def __init__(self, file, gesture_name: str, need_to_capture: int) -> None:
        self._file = file
        self._is_recording = False
        self._gesture_name = gesture_name
        self._captured_count = 0
        self._need_to_capture = need_to_capture

    def capture_hand_landmarks(self, hands_landmarks, hand_num=0) -> None:
        if hands_landmarks:
            hands_landmark_strings = [f"{x},{y}" for x, y in hands_landmarks[hand_num]]
            self._file.write(";".join(hands_landmark_strings))
            self._file.write(f";{self._gesture_name}\n")                      
            self._captured_count += 1

    def all_images_are_captured(self) -> bool:
        if self._captured_count == self._need_to_capture:
            return True
        if self._captured_count > self._need_to_capture:
            raise ValueError(f"{format_exc} Too many gestures were captured.")
        return False

    @property
    def gesture_name(self):
        return self._gesture_name

    @gesture_name.setter
    def gesture_name(self, new_name: str):
        if self.is_recording:
            raise RuntimeError(f"{format_exc} You cannot change gesture name during recording.")
        self.gesture_name = new_name

    @property
    def is_recording(self):
        return self._is_recording

    def start_recoding(self):
        self._is_recording = True

    def end_recording(self):
        self._is_recording = False
