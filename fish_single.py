from fish_main import FishMain
from hsvfilterdto import HsvFilterDTO


class FishSingle:

    def __init__(self, win_name: str, template_file: str, cropped_x: int, cropped_y: int, threshold: float, hsv_filter: HsvFilterDTO):
        """
        :param win_name: None - Без привязки к окну. "Наименование окна" - обрабатывать конкретное окно
        :param template_file: Наименование файла по которому будет поиск. Шаблоны находятся в каталоге img
        :param cropped_x: Подрезать проверяемую область по горизонтали. В пикселях.
        :param cropped_y: Подрезать проверяемую область по вертикали. В пикселях.
        :param threshold: коэффицент точности совпадения
        :param hsv_filter: Объект данных цветовой модели HsvFilterDTO. None - настройка цветодой модели.
        """
        self._template_file = template_file
        self._win_name = win_name
        self._cropped_x = cropped_x
        self._cropped_y = cropped_y
        self._threshold = threshold
        self._hsv_filter = hsv_filter

        self._f_main: FishMain = None
        self._trackbar: bool = False

    def get_fish_main_obj(self) -> FishMain:
        if self._f_main is None:
            self._f_main = FishMain(
                self._win_name,
                self._template_file,
                self._cropped_x,
                self._cropped_y,
                self._threshold,
                self._hsv_filter
            )
            self.set_trackbar_gui()
            return self._f_main
        else:
            return self._f_main

    def clear_fish_main_obj(self):
        self._f_main = None

    def set_trackbar_gui(self):
        if not self._trackbar:
            self._trackbar = self._f_main.vision.init_trackbar_gui()
            # self._trackbar = True
