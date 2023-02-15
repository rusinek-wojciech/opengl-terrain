import noise
import random
from PIL import Image

import numpy
import numpy as np
from sklearn import preprocessing

SCALE = 100
MAP_SIZE = [1000, 1000]

def perlin_nosie(coords, seed):
    return noise.pnoise2(coords[0]/SCALE,
                          coords[1]/SCALE,
                          octaves=7,
                          persistence=0.5,
                          lacunarity=2,
                          repeatx=MAP_SIZE[0],
                          repeaty=MAP_SIZE[1],
                          base=seed
                         )

def generate_heightmap(map_size):
    seed = int(random.random()*1000)
    minimum = 0
    maximum = 0
    heightmap = np.zeros(map_size)

    for x in range(map_size[0]):
        for y in range(map_size[1]):
            new_value = perlin_nosie((x, y), seed)
            heightmap[x][y] = new_value
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

    # The origin and size of mesh
    origin = (-1, -0.75, -1)
    size = 2
    max_height = 0.5

    # We need to calculate the step between vertices
    step_x = size/(heightmap_size[0]-1)
    step_y = size/(heightmap_size[1]-1)

    for x in range(heightmap_size[0]):
        for y in range(heightmap_size[1]):
            x_coord = step_x*x
            y_coord = max_height*heightmap[x][y]
            z_coord = step_y*y
            vertices.append((x_coord, y_coord, z_coord))
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
    size = 1000
    map_size = [size, size]
    heightmap = generate_heightmap(map_size)
    heightmap_expo = expo(heightmap.copy(), map_size, 2)

    new_image = Image.fromarray(heightmap * 255)
    new_image = new_image.convert("L")
    new_image.save('meshes/generated_terrain.png')

    vertices = generate_vertices(heightmap, [size, size])
    tris = generate_tris([size, size])
    export_obj(vertices, tris, filename="meshes/generated_terrain.obj")


