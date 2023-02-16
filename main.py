import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import pyrr
from utils import load_texture
from ObjLoader import ObjLoader

from movement import Movement
from generator import generate

WIDTH, HEIGHT = 1280, 720
IS_RANDOM_TERRAIN = True
movement = Movement(WIDTH, HEIGHT)
terrain_path = "meshes/generated_terrain.obj" if IS_RANDOM_TERRAIN else "meshes/bieszczady_1_2.obj"
texture_path = "meshes/generated_terrain.png" if IS_RANDOM_TERRAIN else "meshes/mapa_kolorowa.jpg"

def window_resize_callback(window, width, height):
    glViewport(0, 0, width, height)
    projection = pyrr.matrix44.create_perspective_projection_matrix(45, width / height, 0.1, 100)
    glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)


vertex_src = """
# version 330

layout(location = 0) in vec3 a_position;
layout(location = 1) in vec2 a_texture;
layout(location = 2) in vec3 a_normal;

uniform mat4 model;
uniform mat4 projection;
uniform mat4 view;

out vec2 v_texture;

void main()
{
    gl_Position = projection * view * model * vec4(a_position, 1.0);
    v_texture = a_texture;
}
"""

fragment_src = """
# version 330

in vec2 v_texture;

out vec4 out_color;

uniform sampler2D s_texture;

void main()
{
    out_color = texture(s_texture, v_texture);
}
"""

if not glfw.init():
    raise Exception("glfw can not be initialized!")

window = glfw.create_window(WIDTH, HEIGHT, "Teren", None, None)

if not window:
    glfw.terminate()
    raise Exception("glfw window can not be created!")

glfw.set_window_size_callback(window, window_resize_callback)
glfw.set_cursor_pos_callback(window, movement.mouse_callback)
glfw.set_key_callback(window, movement.keyboard_callback)
glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
glfw.make_context_current(window)

if IS_RANDOM_TERRAIN:
    generate()

floor_indices, floor_buffer = ObjLoader.load_model(terrain_path)
vertex_shader = compileShader(vertex_src, GL_VERTEX_SHADER)
fragment_shader = compileShader(fragment_src, GL_FRAGMENT_SHADER)
shader = compileProgram(vertex_shader, fragment_shader)

VAO = glGenVertexArrays(2)
VBO = glGenBuffers(2)

glBindVertexArray(VAO[0])
glBindBuffer(GL_ARRAY_BUFFER, VBO[0])
glBufferData(GL_ARRAY_BUFFER, floor_buffer.nbytes, floor_buffer, GL_STATIC_DRAW)

glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, floor_buffer.itemsize * 8, ctypes.c_void_p(0))
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, floor_buffer.itemsize * 8, ctypes.c_void_p(12))
glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, floor_buffer.itemsize * 8, ctypes.c_void_p(20))
glEnableVertexAttribArray(2)

textures = glGenTextures(2)
load_texture(texture_path, textures[0])

glUseProgram(shader)
glClearColor(0.53, 0.8, 0.92, 1)
glEnable(GL_DEPTH_TEST)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

projection = pyrr.matrix44.create_perspective_projection_matrix(45, WIDTH / HEIGHT, 0.1, 100)
floor_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))

model_loc = glGetUniformLocation(shader, "model")
proj_loc = glGetUniformLocation(shader, "projection")
view_loc = glGetUniformLocation(shader, "view")

glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)

while not glfw.window_should_close(window):
    glfw.poll_events()
    movement.do()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glUniformMatrix4fv(view_loc, 1, GL_FALSE, movement.get_view())

    rot_y = pyrr.Matrix44.from_y_rotation(0.8 * glfw.get_time())

    glBindVertexArray(VAO[0])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, floor_pos)
    glDrawArrays(GL_TRIANGLES, 0, len(floor_indices))

    glfw.swap_buffers(window)


glfw.terminate()
