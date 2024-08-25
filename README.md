
# Ray Tracing in Python with Optimization

This project implements a simple ray tracer using Python, **Numpy**, **Matplotlib**, and **Numba** for performance improvements. It supports basic geometric objects like spheres and planes while calculating reflections, diffuse lighting, and specular highlights. The final output is a 1920x1080 image rendered from a scene defined by these objects.

The initial implementation produced a 400x300 resolution image and ran without optimizations. Through performance enhancements and upscaling techniques, the latest version now renders at a higher resolution while maintaining the same ray depth and significantly reducing rendering time.

---

## Features

- **Ray Depth Consistency**: Despite the resolution increase, the ray depth for reflections remains consistent at a maximum of 5.
- **Optimized with Numba**: Numba’s `@njit` decorator drastically improves the performance of key functions, reducing computation time.
- **Supersampling for High Resolution**: The original image is rendered at a lower resolution of 960x540 and then upscaled to 1920x1080 using nearest neighbor interpolation, achieving a high-quality result faster than direct rendering at full resolution.
- **Lighting and Shading**: Includes ambient, diffuse, and specular lighting models for more realistic scenes, along with reflections for both spheres and planes.

---

## Changes and Optimizations

### Resolution Increase:

- **Original Resolution**: 400x300 (120,000 pixels)
- **New Resolution (via supersampling)**: 1920x1080 (2,073,600 pixels)
  
The new resolution is nearly **17.3 times** larger than the original while maintaining consistent ray tracing depth.

- The image is first rendered at a lower resolution (960x540) and then upscaled to 1920x1080 using interpolation. This approach balances quality and speed.
- Even though the upscaled image has over **2 million pixels**, the optimized code ensures that the rendering time is kept minimal.

---

## Performance Comparison

| Version   | Resolution   | Time Taken | Pixel Count | Ray Depth |
|-----------|--------------|------------|-------------|-----------|
| Original  | 400x300      | 4.98 sec   | 120,000     | 5         |
| Optimized | 1920x1080    | 3.35 sec   | 2,073,600   | 5         |

---

### Original Output (400x300)

![raytracing_output2](https://github.com/user-attachments/assets/f06e6e46-d0c4-485a-9024-3e53499f5a45)

---

### Optimized Output (1920x1080)

![raytracing_output](https://github.com/user-attachments/assets/9230d6ee-bc17-4da9-b9f2-87b0f97f53e4)

---

### Preview of V2 with Anti-Aliasing (4k)

| **Resolution**: 3840x2160 | **Pixel Count**: 8,294,400 |

Notice the reduced jagged edges!

![raytracing_output3](https://github.com/user-attachments/assets/efe80799-d72b-4e8f-9f5c-99455eaa84df)

---

## Installation and Usage

### Prerequisites
- Python 3.x
- Required Libraries: `numpy`, `matplotlib`, `numba`

### Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/ray-tracing-optimization.git
   pip install numpy matplotlib numba
   python raytracer.py

