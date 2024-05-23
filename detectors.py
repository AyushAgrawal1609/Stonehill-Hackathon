from cv2.typing import MatLike
from typing import Tuple, Any


class Detector:
    def __init__(self) -> None:
        pass

    def __add__(self, other: "Detector"):
        class DetectorAdd(Detector):
            def __init__(self, obj1: "Detector", obj2: "Detector") -> None:
                pass

    def find(self, img: MatLike) -> Any:
        raise TypeError(
            "A Detector cannot find anything if it does not know what to detect."
        )
