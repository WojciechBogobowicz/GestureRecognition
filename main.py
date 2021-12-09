from HandTrackingModule import HandDetector
from Keyboard import Keyboard, Key
from GestureSaver import GestureSaver
from CameraReader import CameraReader



def main():
    hand_detector = HandDetector()
    camera_reader = CameraReader()

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

        for img in camera_reader.loop_until(gesture_saver.all_images_are_captured):
            img = CameraReader.get_mirror_view(img)
            img = CameraReader.add_label(img, str(gesture_saver))
            img = camera_reader.display_fps(img)
            hand_list = hand_detector.find_hands(img)
            gesture_saver.save_hand_landmarks_if_recording(hand_list)
            camera_reader.display_image(img)



if __name__=="__main__":
    main()