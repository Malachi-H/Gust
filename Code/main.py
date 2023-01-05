import pyglet
from pyglet.window import key

window = pyglet.window.Window()
keys = key.KeyStateHandler()


@window.event
def on_key_press(keys, modifiers):
    # Check if the spacebar is currently pressed:
    print(key.symbol_string(keys))
    # window.push_handlers(keys)


pyglet.app.run()
