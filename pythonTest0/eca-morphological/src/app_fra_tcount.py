import fra_count_tr_class


fra_count_obj = fra_count_tr_class.FractalCountTriangle()
fra_count_obj.image_path = "dilated_image.png"

np_image = fra_count_obj.read_image()
print("Numpy Image Array:")
print(np_image)

print("Getting triangles...")
fra_count_obj.count_triangles_for()

#print(f"Total Triangles Counted:")
#fra_count_obj.draw_lines()
