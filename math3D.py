import numpy as np
from collections.abc import Sequence


def rotateX(X, angle):
    # Rotates object around x axis
    T = np.array([
        [1, 0, 0, 0],
        [0, np.cos(angle), np.sin(angle), 0],
        [0, -np.sin(angle), np.cos(angle), 0],
        [0, 0, 0, 1]
    ])
    return X @ T


def rotateY(X, angle):
    # Rotates object around y axis
    T = np.array([
        [np.cos(angle), 0, -np.sin(angle), 0],
        [0, 1, 0, 0],
        [np.sin(angle), 0, np.cos(angle), 0],
        [0, 0, 0, 1]
    ])
    return X @ T


def rotateZ(X, angle):
    # Rotates object around z axis
    T = np.array([
        [np.cos(angle), np.sin(angle), 0, 0],
        [-np.sin(angle), np.cos(angle), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])
    return X @ T


def rotate(object, axis, angles):
    # Rotates object around given axis
    if isinstance(axis, Sequence) and not isinstance(angles, Sequence):
        angles = [angles for i in range(len(axis))]
    for ax, angle in zip(axis, angles):
        if ax.lower() == 'x':
            object = rotateX(object, angle)
        elif ax.lower() == 'y':
            object = rotateY(object, angle)
        elif ax.lower() == 'z':
            object = rotateZ(object, angle)
    return object


def rotate_around_axis(object, axis, angle):
    object = translate(object)


def translate(object, delta):
    T = np.identity(4)
    T[3, :] = np.concatenate([delta, [1]])
    return object @ T


def scale(object, scale=1):
    T = np.identity(4)
    T[3, 3] = scale
    object = object @ T
    object /= object[:, 3, np.newaxis]
    return object



def project_isometric(object, alpha=-0.25*np.pi, beta=0.62*np.pi):
    # Projects object onto z=0 plane using isometric projection
    proj_matrix = np.identity(4)
    proj_matrix[2, 2] = 0
    projected_object = rotate(object, 'yx', (alpha, beta)) @ proj_matrix
    return projected_object


def project(object, aspectratio, fov, far, near):
    fov_mult = 1 / np.tan(0.5 * fov * np.pi / 180)
    far_mult = far / (far - near)
    proj_matrix = np.array([
        [aspectratio * fov_mult, 0, 0, 0],
        [0, fov_mult, 0, 0],
        [0, 0, far_mult, 1],
        [0, 0, -far_mult * near, 0]
    ])
    object = object @ proj_matrix
    z = object[:, 3, np.newaxis]
    z[z == 0] = 1
    object /= z
    return object


def prepare_for_display(object, width, height):
    object = translate(object, [1, 1, 0])
    scale_matrix = np.identity(4)
    scale_matrix[0, 0] *= 0.5 * width
    scale_matrix[1, 1] *= 0.5 * height
    object = object @ scale_matrix
    return object