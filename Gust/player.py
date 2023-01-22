from ursina import Entity
from ursina import held_keys
from ursina import color


class player_controller(Entity):
    def __init__(self, **kwargs):
        super().__init__()
        for key, value in kwargs.items():
            setattr(self, key, value)

        self.model = "cube"
        self.origin_y = -0.5
        self.scale_y = 2
        self.color = color.orange
        self.collider = "box"

    def update(self):
        pass

    def input(self, key):
        if key == "d":
            self.velocity = 1
            # self.scale_x = self._original_scale_x
        if key == "d up":
            self.velocity = -held_keys["a"]

        if key == "a":
            self.velocity = -1
        if key == "a up":
            self.velocity = held_keys["d"]

        if held_keys["d"] or held_keys["a"]:
            self.scale_x = self._original_scale_x * self.velocity
