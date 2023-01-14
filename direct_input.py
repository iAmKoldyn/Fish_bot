import pydirectinput


class DirectInput:

    @staticmethod
    def move_to(x: int, y: int):
        pydirectinput.moveTo(x, y)

    @staticmethod
    def click():
        pydirectinput.click()

    @staticmethod
    def right_click():
        pydirectinput.click(button='right')

    @staticmethod
    def press_key(key_name: str):
        pydirectinput.press(key_name)
