from ursina import window
from ursina import Ursina
from ursina import camera
from ursina import EditorCamera
from ursina import Entity
from ursina import color
from ursina import held_keys
from ursina import application
from ursina import Vec2
from ursina.main import time
from player import player_controller


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


# def update():
#     ground.y += 1 * time.dt


def update():
    pass


if __name__ == "__main__":
    camera.orthographic = True
    camera.fov = 20

    EditorCamera()

    ground = Entity(
        model="cube",
        scale=(40, 2),
        collider="box",
        color=color.rgb(255, 0, 0),
        position=Vec2(0, -camera.fov / 2),  # bottom of screen
    )

    player = player_controller()

    app.run()
