import numpy as np
from collections.abc import Sequence


def normalize(X):
    if X.ndim == 1:
        norm = X[:3] / np.linalg.norm(X[:3])
        norm = np.concatenate([norm, [1]])
    else:
        norm = X[:, :3] / np.linalg.norm(X[:, :3], axis=-1)[:, None]
        norm = np.pad(norm, [(0, 0), (0, 1)], mode='constant', constant_values=1)
    return norm


def dot(X, y):
    return np.sum(X[:, :3] * y[:3], axis=1)


def get_normal(polygons):
    if polygons.ndim == 2:
        A = polygons[1, :3] - polygons[0, :3]
        B = polygons[2, :3] - polygons[0, :3]
        normal = np.array([
            A[1] * B[2] - A[2] * B[1],
            A[2] * B[0] - A[0] * B[2],
            A[0] * B[1] - A[1] * B[0],
        ])
        normal = np.concatenate([normal, [1]])
        return normal
    elif polygons.ndim == 3:
        A = polygons[:, 1, :3] - polygons[:, 0, :3]
        B = polygons[:, 2, :3] - polygons[:, 0, :3]
        normals = np.array([
            A[:, 1] * B[:, 2] - A[:, 2] * B[:, 1],
            A[:, 2] * B[:, 0] - A[:, 0] * B[:, 2],
            A[:, 0] * B[:, 1] - A[:, 1] * B[:, 0],
        ]).T
        normals = np.pad(normals, [(0, 0), (0, 1)], mode='constant', constant_values=1)
        return normals


def rotateX(X, angle, around=None):
    # Rotates object around given axis (defaults to x-axis)
    if np.isclose(angle, 0):
        return X
    T = np.array([
        [1, 0, 0, 0],
        [0, np.cos(angle), np.sin(angle), 0],
        [0, -np.sin(angle), np.cos(angle), 0],
        [0, 0, 0, 1]
    ])
    if around is None:
        return X @ T
    else:
        X = translate(X, -around)
        X = X @ T
        return translate(X, around)


def rotateY(X, angle, around=None):
    # Rotates object around given axis (defaults to y-axis)
    if np.isclose(angle, 0):
        return X
    T = np.array([
        [np.cos(angle), 0, -np.sin(angle), 0],
        [0, 1, 0, 0],
        [np.sin(angle), 0, np.cos(angle), 0],
        [0, 0, 0, 1]
    ])
    if around is None:
        return X @ T
    else:
        X = translate(X, -around)
        X = X @ T
        return translate(X, around)


def rotateZ(X, angle, around=None):
    # Rotates object around given axis (defaults to z-axis)
    if np.isclose(angle, 0):
        return X
    T = np.array([
        [np.cos(angle), np.sin(angle), 0, 0],
        [-np.sin(angle), np.cos(angle), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])
    if around is None:
        return X @ T
    else:
        X = translate(X, -around)
        X = X @ T
        return translate(X, around)


def translate(object, delta):
    T = np.identity(4)
    if len(delta) == 3:
        delta = np.concatenate([delta, [1]])
    T[3, :] = delta
    return object @ T


def scale(object, scale):
    T = np.identity(4)
    if isinstance(scale, Sequence) and len(scale) == 3:
        np.fill_diagonal(T, np.concatenate([np.array(scale), np.array([1])]))
    else:
        T[3, 3] = 1 / scale
    object = object @ T
    if object.ndim == 2:
        h = object[:, 3, np.newaxis]
    elif object.ndim == 3:
            h = object[:, :, 3, np.newaxis]
    h[h == 0] = 1
    object /= h
    return object


def project_isometric(object, alpha=-0.25*np.pi, beta=0.62*np.pi):
    # Projects object onto z=0 plane using isometric projection
    proj_matrix = np.identity(4)
    proj_matrix[2, 2] = 0
    projected_object = rotateX(rotateY(object, alpha), beta) @ proj_matrix
    return projected_object


def project(object, aspectratio, fov, far, near):
    fov_mult = 1 / np.tan(0.5 * fov * np.pi / 180)
    far_mult = far / (far - near)
    proj_matrix = np.array([
        [aspectratio * fov_mult, 0, 0, 0],
        [0, fov_mult, 0, 0],
        [0, 0, -far_mult, -1],
        [0, 0, -far_mult * near, 0]
    ], dtype=np.float32)
    object = object @ proj_matrix
    if object.ndim == 2:
        h = object[:, 3, np.newaxis]
    elif object.ndim == 3:
        h = object[:, :, 3, np.newaxis]
    h[h == 0] = 1
    object /= h
    return object
