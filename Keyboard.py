from pynput.keyboard import Listener
from sched import scheduler
import threading
from time import time, sleep



class Keyboard:
    def __init__(self, keys_list=[]):
        """
        This obj allows you to bind keys to functions.
        :param key_dict: dict whose keys are str representations of keyboard keys, and values are tuples of three
        functions called when key is respectively pressed, holded and realesed.
        """
        self._keys_dict = dict()
        self.add_keys(keys_list)
        self.last_update = 10
        listener = Listener(on_press=self._behaviour_when_key_is_pressed,
                            on_release=self._behaviour_when_key_is_release)
        listener.start()
        self._monitor_held_keys()

    def _behaviour_when_key_is_pressed(self, read_key):
        """
        This function deals with situation when key is pressed.
        :param read_key: Str name of pressed key.
        :return: None
        """
        key_name = Keyboard.covert_key_to_str(read_key)
        if key_name in self._keys_dict:
            key = self._keys_dict[key_name]
            key.function_on_press()

    def _behaviour_when_key_is_release(self, read_key):
        """
        This function deals with situation when key is released.
        :param read_key: Str name of released key.
        :return: None
        """
        key_name = Keyboard.covert_key_to_str(read_key)
        if key_name in self._keys_dict:
            key = self._keys_dict[key_name]
            key.function_on_release()

    def _monitor_held_keys(self):
        def repeat_checking_held_keys():
            while True:
                self._check_held_keys()
                sleep(0.01)
        t = threading.Thread(name="monitor held keys", target=repeat_checking_held_keys)
        t.setDaemon(True)
        t.start()

    def _check_held_keys(self):
        """
        This function calls functions that are binded to keys of hold-event if they are holded.
        :return: None
        """
        for key in self._keys_dict.values():
            key.check_if_hold_and_deal_with_it()

    def add_keys(self, keys_list):
        """
        This function binds keys to Keyboard.
        :param keys_list: Any iterable object with Keys objects
        :return: None
        """
        for key in keys_list:
            self._keys_dict[key.name] = key

    @staticmethod
    def covert_key_to_str(key):
        return str(key).split(".")[-1].strip("'")


class Key:
    def __init__(self):
        self.name = ""
        self._pressed = self._prepare_press_function(self._empty_function)
        self._hold = self._prepare_hold_function(self._empty_function)
        self._released = self._prepare_release_function(self._empty_function)
        self._is_hold = False

    def function_on_press(self):
        return self._pressed()

    def set_function_on_press(self, function):
        if function == None:
            return
        self._pressed = self._prepare_press_function(function)

    def _prepare_press_function(self, function):
        def new_function(*args, **kwargs):
            if not self._is_hold:
                self._is_hold = True
                return function(*args, **kwargs)
            else:
                return self._empty_function(*args, **kwargs)
        return new_function

    def function_on_release(self):
        return self._released()

    def set_function_on_release(self, function):
        if function == None:
            return
        self._released = self._prepare_release_function(function)

    def _prepare_release_function(self, function):
        def new_function(*args, **kwargs):
            if not self._is_hold:
                raise ValueError("something went wrong, key is not hold")
            self._is_hold = False
            return function(*args, **kwargs)
        return new_function

    def check_if_hold_and_deal_with_it(self):
        self._hold()

    def set_function_on_hold(self, function):
        if function == None:
            return
        self._hold = self._prepare_hold_function(function)

    def _prepare_hold_function(self, function):
        def new_function(*args, **kwargs):
            if not self._is_hold:
                return self._empty_function(*args, **kwargs)
            else:
                return function(*args, **kwargs)
        return new_function

    @staticmethod
    def _empty_function(*args, **kwargs):
        pass


if __name__ == "__main__":
    def a_pressed(): print("a pressed")
    def a_holded(): print("a holded")
    def a_release(): print("a release")
    def s_pressed(): print("b pressed")
    def s_holded(): print("b holded")
    def s_realese(): print("b realese")
    def photo(): print("pstryk")

    #d = {"a": (a_pressed, a_holded, a_release), "s": (s_pressed, s_holded, s_realese)}
    k = Keyboard()
    alt = Key()
    alt.name = "alt"
    alt.set_function_on_press(photo)
    a = Key()
    a.name = "a"
    a.set_function_on_press(a_pressed)
    a.set_function_on_hold(a_holded)
    a.set_function_on_release(a_release)
    k.add_keys((a, alt))
    while True:
        #k.monitor_held_keys()
        pass

