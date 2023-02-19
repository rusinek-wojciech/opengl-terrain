import glfw
from OpenGL.GL import *
import numpy as np
import pyrr
from shader import createShader
from utils import load_texture, load_model
from movement import Movement
from generator import generate

# -----------------------------------------------------------------

WIDTH, HEIGHT = 1280, 720
IS_RANDOM_TERRAIN = False

TERRAIN_PATH = "meshes/bieszczady_1_3.obj"
TEXTURE_PATH = "meshes/mapa_kolorowa.jpg"
RANDOM_PATH = "meshes/generated_terrain.obj"

movement = Movement(WIDTH, HEIGHT)

# -----------------------------------------------------------------

def window_resize(window, width=WIDTH, height=HEIGHT):
    glViewport(0, 0, width, height)
    projection = pyrr.matrix44.create_perspective_projection_matrix(45, width / height, 0.1, 100)
    glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)


if not glfw.init():
    raise Exception("glfw can not be initialized!")

window = glfw.create_window(WIDTH, HEIGHT, "Teren", None, None)

if not window:
    glfw.terminate()
    raise Exception("glfw window can not be created!")

glfw.set_window_size_callback(window, window_resize)
glfw.set_cursor_pos_callback(window, movement.mouse_callback)
glfw.set_key_callback(window, movement.keyboard_callback)
glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
glfw.make_context_current(window)

shader = createShader(IS_RANDOM_TERRAIN)
glUseProgram(shader)

model_loc = glGetUniformLocation(shader, "model")
proj_loc = glGetUniformLocation(shader, "projection")
view_loc = glGetUniformLocation(shader, "view")
view_pos_loc = glGetUniformLocation(shader, "viewPos")
material_diffuse_loc = glGetUniformLocation(shader, "material_diffuse")

window_resize(None)
floor_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))
glUniformMatrix4fv(model_loc, 1, GL_FALSE, floor_pos)
glUniform1i(material_diffuse_loc, 0)

# -----------------------------------------------------------------

if IS_RANDOM_TERRAIN:

    generate()
    terrain_indices, terrain_buffer = load_model(RANDOM_PATH)
    buffer = np.array(terrain_buffer, dtype=np.float32)

    VAO = glGenVertexArrays(2)
    VBO = glGenBuffers(2)

    glBindVertexArray(VAO[0])
    glBindBuffer(GL_ARRAY_BUFFER, VBO[0])
    glBufferData(GL_ARRAY_BUFFER, buffer.nbytes, buffer, GL_STATIC_DRAW)

    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
    glEnableVertexAttribArray(1)

else:

    terrain_indices, terrain_buffer = load_model(TERRAIN_PATH)
    buffer = np.array(terrain_buffer, dtype=np.float32)

    VAO = glGenVertexArrays(2)
    VBO = glGenBuffers(2)

    glBindVertexArray(VAO[0])
    glBindBuffer(GL_ARRAY_BUFFER, VBO[0])
    glBufferData(GL_ARRAY_BUFFER, buffer.nbytes, buffer, GL_STATIC_DRAW)

    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, buffer.itemsize * 8, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, buffer.itemsize * 8, ctypes.c_void_p(12))
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, buffer.itemsize * 8, ctypes.c_void_p(20))
    glEnableVertexAttribArray(2)

    image, image_bytes = load_texture(TEXTURE_PATH)
    textures = glGenTextures(2)

    glBindTexture(GL_TEXTURE_2D, textures[0])
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_bytes)

# -----------------------------------------------------------------

glClearColor(0.53, 0.8, 0.92, 1)
glEnable(GL_DEPTH_TEST)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

while not glfw.window_should_close(window):
    glfw.poll_events()
    movement.do()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glUniformMatrix4fv(view_loc, 1, GL_FALSE, movement.get_view())
    glUniform3f(view_pos_loc, *movement.get_view_position())

    glBindVertexArray(VAO[0])
    glDrawArrays(GL_TRIANGLES, 0, len(terrain_indices))

    glfw.swap_buffers(window)

glfw.terminate()
