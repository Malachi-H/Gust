import re as RegEx

class ScreenDimensions:
    def __init__(self) -> None:
        self.DEFAULT_SCREEN_DIMENSIONS: tuple[int, int] = (720, 480)
        self.screen_dimensions: tuple[int, int] = self.get_saved_screen_dimensions()

    def get_saved_screen_dimensions(self) -> tuple[int, int]:
        with open("custom_settings.txt", "r") as f:
                resolution = RegEx.match(r"Resolution = (\(\d+, \d+\))", f.read())
                if resolution == None:
                    return self.DEFAULT_SCREEN_DIMENSIONS
                else:
                    return eval(resolution.group(1)) # capture string and convert to tuple
    @property
    def scale_factor(self) -> float:
        return self.screen_dimensions[0] / self.DEFAULT_SCREEN_DIMENSIONS[0]
