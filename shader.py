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

out vec2 TexCoords;
out vec3 Normal;
out vec3 FragPos;

void main()
{
    FragPos = vec3(model * vec4(a_position, 1.0));
    Normal = mat3(transpose(inverse(model))) * a_normal;
    TexCoords = a_texture;

    gl_Position = projection * view * vec4(a_position, 1.0);
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

in vec3 FragPos;  
in vec3 Normal;  
in vec2 TexCoords;

out vec4 FragColor;

uniform vec3 viewPos;
uniform sampler2D material_diffuse;

void main()
{
    vec3 material_specular = vec3(0.5f, 0.5f, 0.5f);
    float material_shininess = 64.0f;

    vec3 light_specular = vec3(1.0f, 1.0f, 1.0f);
    vec3 light_ambient = vec3(0.2f, 0.2f, 0.2f);
    vec3 light_position = vec3(1.2f, 1.0f, 2.0f);
    vec3 light_diffuse = vec3(0.5f, 0.5f, 0.5f);

    // ambient
    vec3 ambient = light_ambient * texture(material_diffuse, TexCoords).rgb;

    // diffuse 
    vec3 norm = normalize(Normal);
    vec3 lightDir = normalize(light_position - FragPos);
    float diff = max(dot(norm, lightDir), 0.0);
    vec3 diffuse = light_diffuse * diff * texture(material_diffuse, TexCoords).rgb;  

    // specular
    vec3 viewDir = normalize(viewPos - FragPos);
    vec3 reflectDir = reflect(-lightDir, norm);  
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), material_shininess);
    vec3 specular = light_specular * (spec * material_specular);  
        
    vec3 result = ambient + diffuse + specular;
    FragColor = vec4(result, 1.0);
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
