from typing import Tuple

import numpy as np
import win32con
import win32gui
import win32ui


class WindowCapture:

    def __init__(self, window_name: str, cropped_x: int, cropped_y: int):
        self._hwnd = self._get_window_hwnd(window_name)
        self._cropped_x = cropped_x
        self._cropped_y = cropped_y

        self._win_x, self._win_y, self._w, self._h = self._get_window_size()
        self.offset_x = self._win_x + cropped_x
        self.offset_y = self._win_y + cropped_y
        self._w = self._w - cropped_x * 2
        self._h = self._h - cropped_y - cropped_x

    def _get_window_hwnd(self, window_name):
        if window_name is None:
            return win32gui.GetDesktopWindow()
        else:
            hwnd = win32gui.FindWindow(None, window_name)
            if not hwnd:
                raise Exception(f"Window '{window_name}' not found")
            return hwnd

    def _get_window_size(self) -> Tuple[int, int, int, int]:
        win_x, win_y, win_w, win_h = win32gui.GetWindowRect(self._hwnd)
        return win_x, win_y, (win_w - win_x), (win_h - win_y)

    def get_screenshot(self) -> np.ndarray:
        comp_dc, bit_map, dc_handle, win_dc = self._get_window_image_data()
        img = self._convert_raw_data_into_ocv(bit_map)
        self._clear_resources(comp_dc, bit_map, dc_handle, win_dc)
        return np.ascontiguousarray(img)  # https://github.com/opencv/opencv/issues/14866#issuecomment-580207109

    def _get_window_image_data(self):
        win_dc = win32gui.GetWindowDC(self._hwnd)
        dc_handle = win32ui.CreateDCFromHandle(win_dc)
        comp_dc = dc_handle.CreateCompatibleDC()
        bit_map = win32ui.CreateBitmap()
        bit_map.CreateCompatibleBitmap(dc_handle, self._w, self._h)
        comp_dc.SelectObject(bit_map)
        comp_dc.BitBlt((0, 0), (self._w, self._h), dc_handle, (self._cropped_x, self._cropped_y), win32con.SRCCOPY)
        return comp_dc, bit_map, dc_handle, win_dc

    def _convert_raw_data_into_ocv(self, bit_map):
        img = np.frombuffer(bit_map.GetBitmapBits(True), dtype='uint8')
        img.shape = (self._h, self._w, 4)
        return img

    def _clear_resources(self, comp_dc, bit_map, dc_handle, win_dc):
        comp_dc.DeleteDC()
        dc_handle.DeleteDC()
        win32gui.DeleteObject(bit_map.GetHandle())
        win32gui.ReleaseDC(self._hwnd, win_dc)
