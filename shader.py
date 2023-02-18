from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader

terr_vertex_src = """
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

random_vertex_src = """
# version 330

layout(location = 0) in vec3 a_position;
layout(location = 1) in vec3 a_color;

uniform mat4 model;
uniform mat4 projection;
uniform mat4 view;

out vec3 v_color;

void main()
{
    gl_Position = projection * view * model * vec4(a_position, 1.0);
    v_color = a_color;
}
"""


terr_fragment_src = """
# version 330

in vec2 v_texture;
out vec4 out_color;
uniform sampler2D s_texture;

void main()
{
    out_color = texture(s_texture, v_texture);
}
"""

random_fragment_src = """
# version 330

in vec3 v_color;
out vec4 out_color;

void main()
{
    out_color = vec4(v_color, 1.0f);
}
"""


def createShader(is_random):
    vert = random_vertex_src if is_random else terr_vertex_src
    vertex_shader = compileShader(vert, GL_VERTEX_SHADER)

    frag = random_fragment_src if is_random else terr_fragment_src
    fragment_shader = compileShader(frag, GL_FRAGMENT_SHADER)

    shader = compileProgram(vertex_shader, fragment_shader)
    return shader
