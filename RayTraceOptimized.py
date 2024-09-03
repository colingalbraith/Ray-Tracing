"""
MIT License

Copyright (c) 2017 Cyrille Rossant

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""



import time
import numpy as np
import matplotlib.pyplot as plt
from numba import njit

w = 960  #  res for supersampling
h = 540

# res for supersampling
target_w = 1920
target_h = 1080

@njit
def normalize(x):
    norm = np.linalg.norm(x)
    if norm == 0:
        return x
    return x / norm


@njit
def intersect_plane(O, D, P, N):
    denom = np.dot(D, N)
    if np.abs(denom) < 1e-6:
        return np.inf
    d = np.dot(P - O, N) / denom
    if d < 0:
        return np.inf
    return d


@njit
def intersect_sphere(O, D, S, R):
    a = np.dot(D, D)
    OS = O - S
    b = 2 * np.dot(D, OS)
    c = np.dot(OS, OS) - R * R
    disc = b * b - 4 * a * c
    if disc > 0:
        distSqrt = np.sqrt(disc)
        q = (-b - distSqrt) / 2.0 if b < 0 else (-b + distSqrt) / 2.0
        t0 = q / a
        t1 = c / q
        t0, t1 = min(t0, t1), max(t0, t1)
        if t1 >= 0:
            return t1 if t0 < 0 else t0
    return np.inf


@njit
def get_normal_sphere(M, S):
    return normalize(M - S)


@njit
def get_plane_color(M):
    if (int(M[0] * 2) % 2) == (int(M[2] * 2) % 2):
        return np.array([1.0, 1.0, 1.0])  # White
    else:
        return np.array([0.0, 0.0, 0.0])  # Black


@njit
def trace_ray(rayO, rayD, sphere_positions, sphere_radii, sphere_colors, plane_pos, plane_norm, L, ambient, diffuse_c,
              specular_c, specular_k, color_light, depth_max, cached_L):
    t = np.inf
    obj_idx = -1
    obj_type = -1  # 0 for sphere, 1 for plane

    for i in range(len(sphere_positions)):
        t_obj = intersect_sphere(rayO, rayD, sphere_positions[i], sphere_radii[i])
        if t_obj < t:
            t, obj_idx, obj_type = t_obj, i, 0

    t_plane = intersect_plane(rayO, rayD, plane_pos, plane_norm)
    if t_plane < t:
        t, obj_idx, obj_type = t_plane, -1, 1

    if t == np.inf:
        return None, None, None, 0
    M = rayO + rayD * t
    if obj_type == 0:  # Sphere
        N = get_normal_sphere(M, sphere_positions[obj_idx])
        color = sphere_colors[obj_idx]
        reflection = 0.5  # reflection for spheres
    else:  # Plane
        N = plane_norm
        color = get_plane_color(M)
        reflection = 0.2  #  reflective  for plane

    # Cached light direction
    toL = cached_L
    toO = normalize(rayO - M)

    # Compute shadow
    l_shadow = np.inf
    for i in range(len(sphere_positions)):
        t_shadow = intersect_sphere(M + N * .0001, toL, sphere_positions[i], sphere_radii[i])
        l_shadow = min(l_shadow, t_shadow)
    if l_shadow < np.inf:
        return M, N, np.zeros(3), reflection

    # Lambert shading (diffuse)
    col_ray = ambient + diffuse_c * max(np.dot(N, toL), 0) * color
    # Blinn-Phong shading (specular)
    col_ray += specular_c * max(np.dot(N, normalize(toL + toO)), 0) ** specular_k * color_light

    return M, N, col_ray, reflection


@njit
def render_scene(w, h, sphere_positions, sphere_radii, sphere_colors, plane_pos, plane_norm, S, L, ambient, diffuse_c,
                 specular_c, specular_k, color_light, depth_max, O):
    img = np.zeros((h, w, 3))
    r = float(w) / h
    Q = np.array([0., 0., 0.])  # Camera pos

    # Precompute screen space coordinates
    screen_x = np.linspace(S[0], S[2], w)
    screen_y = np.linspace(S[1], S[3], h)

    #cahce light
    cached_L = normalize(L)

    for i in range(w):
        if i % 10 == 0:
            print(i / float(w) * 100, "%")
        for j in range(h):
            col = np.zeros(3)
            Q[0], Q[1] = screen_x[i], screen_y[j]
            D = normalize(Q - O)
            rayO, rayD = O, D
            reflection = 1.
            for depth in range(depth_max):
                M, N, col_ray, reflection_factor = trace_ray(rayO, rayD, sphere_positions, sphere_radii, sphere_colors,
                                                             plane_pos, plane_norm, L, ambient, diffuse_c, specular_c,
                                                             specular_k, color_light, depth_max, cached_L)
                if M is None:
                    break

                col += reflection * col_ray
                reflection *= reflection_factor

                #next ray
                rayO, rayD = M + N * .0001, normalize(rayD - 2 * np.dot(rayD, N) * N)

            img[h - j - 1, i, :] = np.clip(col, 0, 1)

    return img


def upscale_image(img, target_w, target_h):
    img_upscaled = np.zeros((target_h, target_w, 3))
    scale_x = target_w / img.shape[1]
    scale_y = target_h / img.shape[0]

    for i in range(target_h):
        for j in range(target_w):
            # finds the matching pixel in the lower res img
            orig_x = int(j / scale_x)
            orig_y = int(i / scale_y)
            img_upscaled[i, j, :] = img[orig_y, orig_x, :]

    return img_upscaled


# Setting up the scene using NumPy arrays Numba
sphere_positions = np.array([[.75, .1, 1.], [-.75, .1, 2.25], [-2.75, .1, 3.5]])
sphere_radii = np.array([.6, .6, .6])
sphere_colors = np.array([[0., 0., 1.], [.5, .223, .5], [1., .572, .184]])

plane_pos = np.array([0., -.5, 0.])
plane_norm = np.array([0., 1., 0.])

# lighting / camera set
L = np.array([5., 5., -10.])
color_light = np.ones(3)
ambient = .05
diffuse_c = 1.
specular_c = 1.
specular_k = 50
depth_max = 5
O = np.array([0., 0.35, -1.])

# Screen coords: x0, y0, x1, y1
S = (-1., -1. / (w / h) + .25, 1., 1. / (w / h) + .25)

# timer
start_time = time.time()

# lower img res
img_low_res = render_scene(w, h, sphere_positions, sphere_radii, sphere_colors, plane_pos, plane_norm, S, L, ambient,
                           diffuse_c, specular_c, specular_k, color_light, depth_max, O)

# Upscale
img_upscaled = upscale_image(img_low_res, target_w, target_h)

end_time = time.time()

print(f"Time taken: {end_time - start_time:.2f} seconds")


#plt.imsave('raytracing_output.png', img_upscaled)

plt.imshow(img_upscaled)
plt.axis('off')
plt.show()
