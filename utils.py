import numpy as np

def q_tables():
    # Quantization matrix Q10 (Lower quality, Higher compression)
    # Higher values in the matrix mean more information is discarded
    Q10 = np.array([
        [ 80,  60,  50,  80, 120, 200, 255, 255],
        [ 55,  60,  70,  95, 130, 255, 255, 255],
        [ 70,  65,  80, 120, 200, 255, 255, 255],
        [ 70,  85, 110, 145, 255, 255, 255, 255],
        [ 90, 110, 185, 255, 255, 255, 255, 255],
        [120, 175, 255, 255, 255, 255, 255, 255],
        [245, 255, 255, 255, 255, 255, 255, 255],
        [255, 255, 255, 255, 255, 255, 255, 255]
    ])

    # Quantization matrix Q50 (Medium quality, Medium compression)
    # Values in the matrix are chosen to balance between preserving details and achieving compression
    Q50 = np.array([
        [ 1,  1,  2,  4,  8, 16, 32, 64],
        [ 1,  1,  2,  4,  8, 16, 32, 64],
        [ 2,  2,  2,  4,  8, 16, 32, 64],
        [ 4,  4,  4,  4,  8, 16, 32, 64],
        [ 8,  8,  8,  8,  8, 16, 32, 64],
        [16, 16, 16, 16, 16, 16, 32, 64],
        [32, 32, 32, 32, 32, 32, 32, 64],
        [64, 64, 64, 64, 64, 64, 64, 64]
    ])

    # Quantization matrix Q90 (Higher quality, Lower compression)
    # Lower values preserve more of the high-frequency details
    Q90 = np.array([
        [ 3,  2,  2,  3,  5,  8, 10, 12],
        [ 2,  2,  3,  4,  5, 12, 12, 11],
        [ 3,  3,  3,  5,  8, 11, 14, 11],
        [ 3,  3,  4,  6, 10, 17, 16, 12],
        [ 4,  4,  7, 11, 14, 22, 21, 15],
        [ 5,  7, 11, 13, 16, 12, 23, 18],
        [10, 13, 16, 17, 21, 24, 24, 21],
        [14, 18, 19, 20, 22, 20, 20, 20]
    ])
    
    return Q10, Q50, Q90