import noise
import random
from PIL import Image
import numpy as np
from sklearn import preprocessing

MAP_SIZE = 100
STEP = 10
STEPS = MAP_SIZE * STEP
MAX_HEIGHT = 10

def perlin_noise(x, y, seed):
    return noise.pnoise2(x / STEPS,
                          y / STEPS,
                          octaves=7,
                          persistence=0.5,
                          lacunarity=2,
                          repeatx=MAP_SIZE,
                          repeaty=MAP_SIZE,
                          base=seed
                         )

def generate_heightmap():
    seed = 100 + int(random.random() * 1000)
    heightmap = np.zeros([STEPS, STEPS])
    for y in range(STEPS):
        for x in range(STEPS):
            heightmap[y][x] = perlin_noise(x, y, seed)
    min_max_scaler = preprocessing.MinMaxScaler()
    return min_max_scaler.fit_transform(heightmap)


def generate_vertices(heightmap):
    vertices = []
    for x in range(STEPS):
        for y in range(STEPS):
            point = (x / STEP, MAX_HEIGHT * heightmap[x][y], y / STEP)
            vertices.append(point)
    return vertices

def generate_triangles():
    triangles = []
    for x in range(STEPS - 1):
        for y in range(STEPS - 1):
            index = x * STEPS + y
            a = index
            b = index + 1
            c = index + STEPS + 1
            d = index + STEPS
            triangles.append((a, b, c))
            triangles.append((a, c, d))
    return triangles

def export_obj(vertices, triangles, filename):
    file = open(filename, "w")
    for v in vertices:
      file.write("v " + str(v[0]) + " " + str(v[1]) + " " + str(v[2]) + "\n")
    for t in triangles:
      file.write("f " + str(t[2] + 1) + " " + str(t[1] + 1) + " " + str(t[0] + 1) + "\n")
    file.close()
    return


def generate_model(heightmap):
    vertices = generate_vertices(heightmap)
    triangles = generate_triangles()
    export_obj(vertices, triangles, filename="meshes/generated_terrain.obj")


def generate_image(heightmap):
    heightmap_RGB = np.zeros((STEPS, STEPS, 3), 'uint8')
    for x in range(STEPS):
        for y in range(STEPS):
            heightmap_RGB[x, y, 0] = 0
            heightmap_RGB[x, y, 1] = heightmap[x, y] * 255
            heightmap_RGB[x, y, 2] = 0
    new_image = Image.fromarray(heightmap_RGB, mode='RGB')
    new_image.save('meshes/generated_terrain.png')


def generate():
    heightmap = generate_heightmap()
    generate_model(heightmap)
    generate_image(heightmap)


if __name__ == "__main__":
    generate()

