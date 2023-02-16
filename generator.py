import noise
import random
from PIL import Image

import numpy
import numpy as np
from sklearn import preprocessing

SIZE = 1000
SIZES = [SIZE, SIZE]

def perlin_nosie(x, y, seed):
    return noise.pnoise2(x / SIZE,
                          y / SIZE,
                          octaves=7,
                          persistence=0.5,
                          lacunarity=2,
                          repeatx=SIZES[0],
                          repeaty=SIZES[1],
                          base=seed
                         )

def generate_heightmap(map_size):
    seed = int(random.random()*1000)
    heightmap = np.zeros(map_size)

    for y in range(map_size[0]):
        for x in range(map_size[1]):
            new_value = perlin_nosie(x, y, seed)
            heightmap[y][x] = new_value
    min_max_scaler = preprocessing.MinMaxScaler()
    return min_max_scaler.fit_transform(heightmap)



# exponentional function
def expo(heightmap, heightmap_size, e):
    for x in range(heightmap_size[0]):
        for y in range(heightmap_size[1]):
            heightmap[x][y] = heightmap[x][y]**e
    min_max_scaler = preprocessing.MinMaxScaler()
    return min_max_scaler.fit_transform(heightmap)

def generate_vertices(heightmap, heightmap_size):
    vertices = []
    size = 1000
    max_height = 100

    # We need to calculate the step between vertices
    step_x = size / heightmap_size[0]
    step_y = size / heightmap_size[1]

    for x in range(heightmap_size[0]):
        for y in range(heightmap_size[1]):
            point = (step_x * x, max_height * heightmap[x][y], step_y * y)
            vertices.append(point)

    return vertices

def generate_tris(grid_size):
    tris = []
    for x in range(grid_size[0]-1):
        for y in range(grid_size[1]-1):
            index = x*grid_size[0]+y
            a = index
            b = index+1
            c = index+grid_size[0]+1
            d = index+grid_size[0]
            tris.append((a, b, c))
            tris.append((a, c, d))
    return tris

def export_obj(vertices, tris, filename):
    file = open(filename, "w")
    for vertex in vertices:
      file.write("v " + str(vertex[0]) + " " + str(vertex[1]) + " " + str(vertex[2]) + "\n")
    for tri in tris:
      file.write("f " + str(tri[2]+1) + " " + str(tri[1]+1) + " " + str(tri[0]+1) + "\n")
    file.close()
    return


def generate():
    heightmap = generate_heightmap(SIZES)
    heightmap_expo = expo(heightmap.copy(), SIZES, 2)

    new_image = Image.fromarray(heightmap * 255)
    new_image = new_image.convert("L")
    new_image.save('meshes/generated_terrain.png')

    vertices = generate_vertices(heightmap, SIZES)
    tris = generate_tris(SIZES)
    export_obj(vertices, tris, filename="meshes/generated_terrain.obj")


if __name__ == "__main__":
    generate()
