from dataclasses import dataclass

class ScreenDimensions:
    def __init__(self, screen_dimensions=(720, 480)) -> None:
        self.DEFAULT_SCREEN_DIMENSIONS: tuple[int, int] = (720, 480)
        self.screen_dimensions: tuple[int, int] = screen_dimensions

    @property
    def scale_factor(self) -> float:
        return self.screen_dimensions[0] / self.DEFAULT_SCREEN_DIMENSIONS[0]
