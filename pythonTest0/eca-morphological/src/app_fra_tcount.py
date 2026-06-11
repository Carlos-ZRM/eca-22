import fra_count_tr_class


fra_count_obj = fra_count_tr_class.FractalCountTriangle()
fra_count_obj.image_path = "dilated_image.png"
#fra_count_obj.image_path = "CA_history_rule_22.png"

np_image = fra_count_obj.read_image()

#print("Numpy Image Array:")
print(np_image)

print("Getting lines...")
fra_count_obj.count_lines_for()

print("Total Lines Counted:")
fra_count_obj.draw_lines()

print("Getting triangles...")
fra_count_obj.count_triangles_for()

fra_count_obj.draw_triangles()