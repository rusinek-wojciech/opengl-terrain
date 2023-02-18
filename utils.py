from OpenGL.GL import *
from PIL import Image

def load_texture(path):
    image = Image.open(path).transpose(Image.FLIP_TOP_BOTTOM)
    image_bytes = image.convert("RGBA").tobytes()
    return image, image_bytes


def load_model(file):
    buffer = []
    vertices = []
    textures = []
    normals = []
    all_indices = []
    indices = []


    is_first = True
    f_format = -1

    with open(file, 'r') as f:
        line = f.readline()
        while line:
            values = line.split()
            if values[0] == 'v':
                for value in values[1:]:
                    vertices.append(float(value))

            elif values[0] == 'vt':
                for value in values[1:]:
                    textures.append(float(value))

            elif values[0] == 'vn':
                for value in values[1:]:
                    normals.append(float(value))

            elif values[0] == 'f':
                for value in values[1:]:
                    vals = value.split('/')

                    if is_first:
                        f_format = len(vals)
                        is_first = False

                    for v in vals:
                        all_indices.append(int(v) - 1)
                    indices.append(int(vals[0]) - 1)

            line = f.readline()


    if f_format == 1:
        for i, ind in enumerate(all_indices):
            start = ind * 3
            end = start + 3
            buffer.extend(vertices[start:end])
            buffer.extend([0.5, 0.5])
            buffer.extend([0.0, 0.0, 0.0])
    elif f_format == 2:
        for i, ind in enumerate(all_indices):
            if i % 2 == 0:
                start = ind * 3
                end = start + 3
                buffer.extend(vertices[start:end])
            elif i % 2 == 1:
                start = ind * 2
                end = start + 2
                buffer.extend(textures[start:end])
                buffer.extend([0.0, 0.0, 0.0])
    elif f_format == 3:
        for i, ind in enumerate(all_indices):
            if i % 3 == 0:
                start = ind * 3
                end = start + 3
                buffer.extend(vertices[start:end])
            elif i % 3 == 1:
                start = ind * 2
                end = start + 2
                buffer.extend(textures[start:end])
            elif i % 3 == 2:
                start = ind * 3
                end = start + 3
                buffer.extend(normals[start:end])

    return indices, buffer
