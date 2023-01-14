import time
from typing import Tuple, List

from direct_input import DirectInput
from hsvfilterdto import HsvFilterDTO
from py_auto_gui import PyAutoGui
from vision import Vision
from windowcapture import WindowCapture


class FishMain:
    DELTA: int = 7 # Разница пикселей (по вертикали), при которых считать что рыба клюёт.

    def __init__(self, win_name: str, template_name: str, cropped_x: int, cropped_y: int, threshold: float, hsv_filter: HsvFilterDTO):
        self.wincap = WindowCapture(win_name, cropped_x, cropped_y)
        self.vision = Vision(template_name, threshold)
        self.hsv_filter = hsv_filter
        self.control = PyAutoGui() # Использование win32 для функций управления устройств ввода
        # self.control = DirectInput() # Использование direct input для функций управления устройств ввода

        self.minimum = self.maximum = None
        self.screenshot = None
        self.rectangles: List[Tuple[int, int, int, int]] = None
        self.h = self.w = None

        self.processed_image = None

    def run(self):
        self._set_screenshot()
        self._set_processed_image()
        self._set_rectangles()
        self._set_min_max_position()
        # Для настройки
        self.vision.show_debug_window("Matches", self.screenshot, self.rectangles) # Окно без обработки hcv
        self.vision.show_debug_window("Processed", self.processed_image, self.rectangles) # Окно обработанное через hcv
        # self._print_rectangels()

    def _set_screenshot(self):
        self.screenshot = self.wincap.get_screenshot()

    def _set_rectangles(self):
        self.rectangles = self.vision.find(self.processed_image)
        if self.rectangles.any():
            self.h = self.rectangles[0][1]
            self.w = self.rectangles[0][0]

    def _set_processed_image(self):
        self.processed_image = self.vision.apply_hsv_filter(self.screenshot, self.hsv_filter)

    @staticmethod
    def _get_delta(maximum: int, minimum: int) -> int:
        return maximum - minimum if minimum is not None else 0

    def _set_min_max_position(self):
        if self.minimum is None:
            self.minimum = self.maximum = self.h
        else:
            if self.minimum > self.h:
                self.minimum = self.h
            if self.maximum < self.h:
                self.maximum = self.h

    def catch_fish(self) -> bool:
        if self._get_delta(self.maximum, self.minimum) > self.DELTA:
            try:
                self._print_rectangels()
                self.control.move_to(self.w + self.wincap.offset_x, self.h + self.wincap.offset_y + 25)
                self.control.right_click()
            except IndexError:
                pass
            else:
                time.sleep(7)
                self.control.press_key("4")
                return True

    def _print_rectangels(self):
        try:
            print(self.rectangles[0], self.minimum, self.maximum, self._get_delta(self.maximum, self.minimum))
        except IndexError:
            pass
