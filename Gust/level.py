from ursina import Entity
from ursina import color
from ursina import Vec2
from ursina import camera

camera.fov = 20

print(camera.fov)


class levelBase(Entity):
    def __init__(self, add_to_scene_entities=True, **kwargs):
        super().__init__(add_to_scene_entities, **kwargs)


ground = Entity(
    model="cube",
    collider="box",
    scale=(40, 2),
    color=color.rgb(255, 0, 0),
    position=Vec2(0, -camera.fov / 2),  # bottom of screen
)
print(camera.fov)
