"""
Requirements
- python 3.8 or newer
- torch and torchvision stable version
more information: https://github.com/danielgatis/rembg
"""

from rembg.bg import remove
import numpy as np
import io
from PIL import Image

input_path = "/Users/tiger/Downloads/images/IMG_5679.PNG"
output_path = "out.png"

f = np.fromfile(input_path)
result = remove(f)
img = Image.open(io.BytesIO(result)).convert("RGBA")
img.save(output_path)
