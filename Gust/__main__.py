from ursina import *

app = Ursina()
window.title = "Gust"


def update():
    pass


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
