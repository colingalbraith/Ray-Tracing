Ray Tracing in Python with Optimization

This project implements a simple ray tracer using Python, Numpy, Matplotlib, and Numba for performance improvements. The ray tracer supports basic geometric objects like spheres and planes, calculating reflections, diffuse lighting, and specular highlights. The final output is a 1920x1080 image rendered from a scene defined by these objects.

The initial implementation produced a 400x300 resolution image and ran without optimizations. Through performance enhancements and supersampling techniques, the latest version now renders at a higher resolution while maintaining the same ray depth and significantly reducing rendering time.

Features
Ray Depth Consistency: Despite the resolution increase, the ray depth for reflections remains the same at a maximum of 5.
Optimized with Numba: By using Numba’s @njit decorator, the performance of key functions has been drastically improved, reducing computation time.
Supersampling for High Resolution: The original image is rendered at a lower resolution of 960x540 and then upscaled to 1920x1080 using interpolation, achieving a high-quality result faster than direct rendering at full resolution.
Lighting and Shading: The ray tracer includes ambient, diffuse, and specular lighting models for more realistic scenes, along with reflections for both spheres and planes.
Changes and Optimizations
Resolution Increase:

Original Resolution: 400x300 (120,000 pixels)
New resolution (via supersampling): 1920x1080 (2,073,600 pixels)
The new resolution is nearly 17.3 times larger than the original while maintaining consistent ray tracing depth.
Performance Optimizations:

The ray tracing calculations are now optimized using Numba, allowing just-in-time compilation and faster loop execution.
The rendering process for the lower-resolution image (960x540) runs significantly faster due to these optimizations.
Supersampling and Upscaling:

The image is first rendered at a lower resolution (960x540) and then upscaled to 1920x1080 using interpolation. This approach balances quality and speed.
Even though the upscaled image has over 2 million pixels, the optimized code ensures that the rendering time is kept minimal.



Original |
Resolution: 400x300 | Time taken: 4.98 seconds | 120,000 pixels | Ray Depth 5 |

![raytracing_output2](https://github.com/user-attachments/assets/f06e6e46-d0c4-485a-9024-3e53499f5a45)



Optimized |
Resolution: 1920x1080 | Time taken: 3.35 seconds | 2,073,600 pixels | Ray Depth 5 |

![raytracing_output](https://github.com/user-attachments/assets/9230d6ee-bc17-4da9-b9f2-87b0f97f53e4)


