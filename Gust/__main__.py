from ursina import window
from ursina import Ursina
from ursina import camera
from ursina import EditorCamera
from ursina import Entity
from ursina import color
from ursina import held_keys
from ursina import application
from ursina.main import time


app = Ursina()
window.title = "Gust"
window.borderless = False
window.fps_counter.enabled = False
window.exit_button.enabled = False


def pause_handler_input(key):
    # Toggle pause when escape key is pressed
    if key == "escape":
        application.paused = not application.paused


pause_handler = Entity(
    ignore_paused=True, input=pause_handler_input
)  # used to receive input despite game being paused as 'pause_handler' ignores pauses


def update():
    ground.rotation_x += 20 * time.dt
    ground.rotation_y += 200 * time.dt
    ground.rotation_z += 200 * time.dt


if __name__ == "__main__":
    camera.orthographic = True
    camera.fov = 10

    EditorCamera()

    ground = Entity(
        model="cube",
        origin_y=0.5,
        scale=(2, 2),
        collider="box",
        # red color
        color=color.rgb(255, 0, 0),
        position=(0, 0, 0),
        texture="white_cube",
        y=1,
    )

    app.run()
