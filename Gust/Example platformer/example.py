from ursina import *

app = Ursina()

from ursina.prefabs.platformer_controller_2d import PlatformerController2d

player = PlatformerController2d(y=1, z=0.01, scale_y=1, max_jumps=2)

ground = Entity(model="quad", scale_x=10, collider="box", color=color.black)

if __name__ == "__main__":
    app.run()
