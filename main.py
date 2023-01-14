import time

from fish_single import FishSingle
from hsvfilterdto import HsvFilterDTO

if __name__ == '__main__':
    f_single = FishSingle(
        # win_name=None,
        win_name="World of Warcraft",
        template_file='feather.jpg',
        cropped_x=400,
        cropped_y=350,
        threshold=0.6,
        # hsv_filter=HsvFilterDTO(
        #     hMin=96, hMax=147,
        #     sMin=0, sMax=255, sAdd=0, sSub=255,
        #     vMin=0, vMax=255, vAdd=255, vSub=0),
        hsv_filter=None
    )
    start_time = time.time()

    while True:
        f_main = f_single.get_fish_main_obj()
        f_main.run()

        if f_main.catch_fish() or (time.time() - start_time) > 20:
            f_single.clear_fish_main_obj()
            start_time = time.time()

        if f_main.vision.destroy_img():
            break
