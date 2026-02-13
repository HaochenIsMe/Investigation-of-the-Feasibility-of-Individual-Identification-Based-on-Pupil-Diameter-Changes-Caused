import numpy as np
from PIL import Image
import random

# 加载图像
img = Image.open("Images\\Experiment2\\Stimulus8\\Front.png").convert("RGB")
arr = np.array(img)  # shape: (H, W, 3)

# 展平为一维像素数组
pixels = arr.reshape(-1, 3)

num_iterations = 5_000_000

for _ in range(num_iterations):
    i, j = random.randint(0, len(pixels)-1), random.randint(0, len(pixels)-1)
    pixels[i], pixels[j] = pixels[j].copy(), pixels[i].copy()

# 恢复回原尺寸
shuffled_arr = pixels.reshape(arr.shape)

Image.fromarray(shuffled_arr).save("shuffled.png")

print("Done")