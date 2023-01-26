from ursina import Entity
from ursina import held_keys
from ursina import color
from ursina.main import time
from level import ground


class player_controller(Entity):
    def __init__(self, **kwargs):
        super().__init__()
        for key, value in kwargs.items():
            setattr(self, key, value)

        self.model = "cube"
        self.collider = "box"
        self.origin_y = 0.5
        self.scale_y = 2
        self.color = color.orange
        self.gravity = 1

    def update(self):
        self.y -= self.gravity * time.dt

        if player_controller.intersects(ground, debug=True).hit:
            self.y += self.gravity * time.dt

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
            self.scale_x = -self.scale.x
