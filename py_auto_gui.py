import pyautogui


class PyAutoGui:

    @staticmethod
    def move_to(x: int, y: int):
        pyautogui.moveTo(x, y, duration=0.25)

    @staticmethod
    def click():
        pyautogui.click()

    @staticmethod
    def right_click():
        pyautogui.click(button='right')

    @staticmethod
    def press_key(key_name: str):
        pyautogui.press(key_name)
