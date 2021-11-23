import os
import numpy as np
from PIL import Image

session_path = f"./PlayerSessions/{0}/"
if not os.path.isdir(session_path):
    os.mkdir(session_path)

field = []
width = 10
height = 20
for i in range(height):
    new_line = []
    for j in range(width):
        new_line.append((0, 0, 0) if i > height // 2 and j > width // 2 else (1, 0, 0))
    field.append(new_line)

npfield = np.array(field)

new_im = Image.fromarray(np.uint8(npfield * 255))
new_im.save(session_path + "test.bmp")
