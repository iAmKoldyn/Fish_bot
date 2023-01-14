from dataclasses import dataclass


@dataclass
class HsvFilterDTO:
    # Hue — цвет (оттенок)
    hMin: int = None
    hMax: int = None
    # Saturation — насыщенность
    sMin: int = None
    sMax: int = None
    sAdd: int = None
    sSub: int = None
    # Value — яркость
    vMin: int = None
    vMax: int = None
    vAdd: int = None
    vSub: int = None
