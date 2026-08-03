"""Example script for creating an ECA_MM object and applying all morphological operations."""

import ca_mm_class
import numpy as np

kernel_custom = np.array(
    [[0, 0, 0, 1, 0, 0, 0], [0, 0, 1, 1, 1, 0, 0], [0, 1, 0, 0, 0, 1, 0], [1, 1, 1, 0, 1, 1, 1]],
    np.uint8,
)
kernel_custom = np.array([[0, 1, 0], [1, 1, 1]], np.uint8)
eca = ca_mm_class.EcaMm(rule_number=22)

#eca.define_evolution_config(size=80, evolutions=30, print_method="png_file", init_method="single_cell", )
#eca.define_evolution_config(size=1000, evolutions=600, print_method="png_file", init_method="random", )

eca.define_evolution_config(size=150, evolutions=90, print_method="png_file", init_method="seed", seed="11111" )



eca.set_kernel(kernel_custom)
eca.set_iterations(2)
eca.set_pixel_size(4)
eca.rdensity = 0.3
eca.evolution()

eca.print_history()

eca.dilation()
eca.erosion()
eca.gradation()
eca.black_hat()
eca.print_history()
