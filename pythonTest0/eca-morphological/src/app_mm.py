"""Example script for creating an ECA_MM object and applying all morphological operations."""

import ca_mm_class
import numpy as np

kernel_custom = np.array(
    [[0, 0, 0, 1, 0, 0, 0], [0, 0, 1, 1, 1, 0, 0], [0, 1, 0, 0, 0, 1, 0], [1, 1, 1, 0, 1, 1, 1]],
    np.uint8,
)
kernel_custom = np.array([[0, 1, 0], [1, 1, 1]], np.uint8)
eca = ca_mm_class.EcaMm(rule_number=22)
eca.define_evolution_config(size=500, evolutions=500, print_method="png_file", init_method="single_cell", )
#eca.define_evolution_config(size=20, evolutions=10, print_method="png_file", init_method="random", )

eca.set_kernel(kernel_custom)
eca.set_iterations(2)
eca.evolution()

eca.print_history()

eca.dilation()
eca.erosion()
eca.gradation()
eca.black_hat()
eca.print_history()
