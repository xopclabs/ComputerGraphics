import numpy as np


def obj_to_coords(path):
    vertices = []
    faces = []
    # Coordinates of polygons
    coords = []
    with open(path, 'r') as file:
       for line in file.readlines():
            line = line.split()
            if line == []:
                continue
            if line[0] == 'v':
                vertices.append([float(x) for x in line[1:]])
            elif line[0] == 'f':
                data = [int(x.split('/')[0]) - 1 for x in line[1:]]
                fix_negatives = lambda x: -1 if x <= -2 else x
                faces.append([fix_negatives(x) for x in data])
    for poly in faces:
        coords.append([vertices[i] for i in poly[:3]])
    coords = np.array(coords)
    coords = np.pad(coords, ((0, 0), (0, 0), (0, 1)), mode='constant', constant_values=1)
    return coords