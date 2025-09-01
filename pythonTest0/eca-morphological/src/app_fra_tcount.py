import fra_count_tr_class
import numpy as np


fra_count_obj = fra_count_tr_class.FractalCountTriangle()
fra_count_obj.image_path = "dilated_image.png"

np_image = fra_count_obj.read_image()
print(np_image)
fra_count_obj.count_triangles()
