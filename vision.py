from typing import Tuple, List

import cv2 as cv
import numpy as np

from hsvfilterdto import HsvFilterDTO


class Vision:
    TRACKBAR_TITLE = "Trackbars"

    def __init__(self, template_img_path: str, threshold: float):
        self.template_img = self._get_template_img(template_img_path)
        self.template_w, self.template_h = self._get_height_width_template_img()

        self.method = cv.TM_CCOEFF_NORMED
        self.threshold = threshold
        self.size_window_trackbar = 450, 450

    def _get_template_img(self, needle_img_path: str):
        return cv.imread(f"imgs/{needle_img_path}", cv.IMREAD_UNCHANGED)

    def _get_height_width_template_img(self) -> Tuple[int, int]:
        height, width, channels = self.template_img.shape
        return height, width

    def find(self, haystack_img: np.ndarray, max_results: int = 5) -> np.ndarray:
        locations = self._get_locations(haystack_img)

        if not locations:
            return np.array([], dtype=np.int32).reshape(0, 4)  # пустой массив [[1,2,3,4], ...]

        # -----------------------------return locations--------------------------------------------

        rectangles = self._group_rectangles(locations)

        if len(rectangles) > max_results:
            print(f"Find results > {max_results}")
            rectangles = rectangles[:max_results]

        return rectangles

    def _group_rectangles(self, locations: List[Tuple[int, int]]) -> np.ndarray:
        """Группировка близко находящихся найденных блоков в один"""
        rectangles = []
        for x, y in locations:
            rect = [x, y, self.template_w, self.template_h]
            rectangles.append(rect)
            rectangles.append(rect)
        rectangles, weights = cv.groupRectangles(rectangles, groupThreshold=1, eps=0.5)
        return rectangles

    def _get_locations(self, haystack_img: np.ndarray) -> List:
        result = cv.matchTemplate(haystack_img, self.template_img, self.method)
        locations = np.where(result >= self.threshold)
        return list(zip(*locations[::-1]))

    @staticmethod
    def draw_rectangles(haystack_img: np.ndarray, rectangles: List[Tuple[int, int, int, int]]):
        line_color = (0, 255, 0)
        line_type = cv.LINE_4

        for x, y, w, h in rectangles:
            top_left = (x, y)
            bottom_right = (x + w, y + h)
            cv.rectangle(haystack_img, top_left, bottom_right, line_color, lineType=line_type)

        return haystack_img

    def show_debug_window(self, win_name: str, image: np.ndarray, rectangles: List[Tuple[int, int, int, int]] = None):
        if rectangles is not None:
            output_image = self.draw_rectangles(image, rectangles)
            cv.imshow(win_name, output_image)
        else:
            cv.imshow(win_name, image)

    def init_trackbar_gui(self) -> bool:
        cv.namedWindow(self.TRACKBAR_TITLE, cv.WINDOW_NORMAL)
        cv.resizeWindow(self.TRACKBAR_TITLE, *self.size_window_trackbar)

        self._create_hue_trackbar()
        self._create_saturation_trackbar()
        self._create_value_trackbar()
        return True

    def _create_hue_trackbar(self):
        H = 179
        cv.createTrackbar('HMin', self.TRACKBAR_TITLE, 0, H, self.pass_func)
        cv.createTrackbar('HMax', self.TRACKBAR_TITLE, 0, H, self.pass_func)
        cv.setTrackbarPos('HMax', self.TRACKBAR_TITLE, H)

    def _create_saturation_trackbar(self):
        S = 255
        cv.createTrackbar('SMin', self.TRACKBAR_TITLE, 0, S, self.pass_func)
        cv.createTrackbar('SMax', self.TRACKBAR_TITLE, 0, S, self.pass_func)
        cv.setTrackbarPos('SMax', self.TRACKBAR_TITLE, S)

        cv.createTrackbar('SAdd', self.TRACKBAR_TITLE, 0, S, self.pass_func)
        cv.createTrackbar('SSub', self.TRACKBAR_TITLE, 0, S, self.pass_func)

    def _create_value_trackbar(self):
        V = 255
        cv.createTrackbar('VMin', self.TRACKBAR_TITLE, 0, V, self.pass_func)
        cv.createTrackbar('VMax', self.TRACKBAR_TITLE, 0, V, self.pass_func)
        cv.setTrackbarPos('VMax', self.TRACKBAR_TITLE, V)

        cv.createTrackbar('VAdd', self.TRACKBAR_TITLE, 0, V, self.pass_func)
        cv.createTrackbar('VSub', self.TRACKBAR_TITLE, 0, V, self.pass_func)

    @staticmethod
    def pass_func(_):
        pass

    def apply_hsv_filter(self, original_image: np.ndarray, hsv_filter: HsvFilterDTO = None):
        hsv_img = self.convert_img(original_image, cv.COLOR_BGR2HSV)

        if not hsv_filter:
            hsv_filter = self._get_hsv_filter_from_controls()

        hsv = self.__add_sub_saturation_and_value(hsv_img, hsv_filter)
        lower, upper = self.__get_min_max_hsv_filter(hsv_filter)

        mask = cv.inRange(hsv, lower, upper)
        result = cv.bitwise_and(hsv, hsv, mask=mask)

        return self.convert_img(result, cv.COLOR_HSV2BGR)

    @staticmethod
    def convert_img(original_image: np.ndarray, convert_type: str) -> np.ndarray:
        return cv.cvtColor(original_image, convert_type)

    def _get_hsv_filter_from_controls(self) -> HsvFilterDTO:
        """Управление настройками HSV"""
        hsv_filter = HsvFilterDTO()
        hsv_filter.hMin = cv.getTrackbarPos('HMin', self.TRACKBAR_TITLE)
        hsv_filter.hMax = cv.getTrackbarPos('HMax', self.TRACKBAR_TITLE)
        hsv_filter.sMin = cv.getTrackbarPos('SMin', self.TRACKBAR_TITLE)
        hsv_filter.sMax = cv.getTrackbarPos('SMax', self.TRACKBAR_TITLE)
        hsv_filter.sAdd = cv.getTrackbarPos('SAdd', self.TRACKBAR_TITLE)
        hsv_filter.sSub = cv.getTrackbarPos('SSub', self.TRACKBAR_TITLE)
        hsv_filter.vMin = cv.getTrackbarPos('VMin', self.TRACKBAR_TITLE)
        hsv_filter.vMax = cv.getTrackbarPos('VMax', self.TRACKBAR_TITLE)
        hsv_filter.vAdd = cv.getTrackbarPos('VAdd', self.TRACKBAR_TITLE)
        hsv_filter.vSub = cv.getTrackbarPos('VSub', self.TRACKBAR_TITLE)
        return hsv_filter

    def __add_sub_saturation_and_value(self, hsv_img: np.ndarray, hsv_filter: HsvFilterDTO) -> np.ndarray:
        h, s, v = cv.split(hsv_img)
        s = self.__hsv_correction_channel(s, hsv_filter.sAdd)
        s = self.__hsv_correction_channel(s, -hsv_filter.sSub)
        v = self.__hsv_correction_channel(v, hsv_filter.vAdd)
        v = self.__hsv_correction_channel(v, -hsv_filter.vSub)
        return cv.merge([h, s, v])

    def __get_min_max_hsv_filter(self, hsv_filter: HsvFilterDTO) -> Tuple[np.ndarray, np.ndarray]:
        lower = np.array([hsv_filter.hMin, hsv_filter.sMin, hsv_filter.vMin])
        upper = np.array([hsv_filter.hMax, hsv_filter.sMax, hsv_filter.vMax])
        return lower, upper

    # https://stackoverflow.com/questions/49697363/shifting-hsv-pixel-values-in-python-using-numpy
    @staticmethod
    def __hsv_correction_channel(c: np.ndarray, amount: int) -> np.ndarray:
        """Корректировка к HSV"""
        if amount > 0:
            lim = 255 - amount
            c[c >= lim] = 255
            c[c < lim] += amount
        elif amount < 0:
            amount = -amount
            lim = amount
            c[c <= lim] = 0
            c[c > lim] -= amount
        return c

    @staticmethod
    def destroy_img() -> bool:
        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            return True
