from cv2.typing import MatLike
from typing import Tuple, Any


class Detector:
    def __init__(self) -> None:
        pass

    def __add__(self, other: "Detector"):
        class DetectorAdd(Detector):
            def __init__(self, obj1: "Detector", obj2: "Detector") -> None:
                self.obj1 = obj1
                self.obj2 = obj2

            def find(self, img: MatLike) -> Tuple[Any, Any]:
                item1 = self.obj1.find(img)
                item2 = self.obj2.find(img)
                return (item1, item2)

            def draw(self, img: MatLike, res: Tuple[Any, Any]) -> MatLike:
                self.obj1.draw(img, res[0])
                self.obj2.draw(img, res[1])
                return img

        return DetectorAdd(self, other)

    def find(self, img: MatLike) -> Any:
        raise TypeError(
            "A Detector cannot find anything if it does not know what to detect."
        )

    def draw(self, img: MatLike, res) -> MatLike:
        raise TypeError(
            "A Detector cannot find anything if it does not know what to detect."
        )
