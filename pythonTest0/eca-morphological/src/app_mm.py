"""Example script for creating an ECA_MM object and applying all morphological operations."""

import ca_mm_object

eca = ca_mm_object.EcaMm(rule_number=22)
eca.define_evolution_config(size=500, evolutions=500, print_method="png")
eca.evolution()
eca.dilation()
eca.erosion()
eca.gradation()
eca.black_hat()
eca.print_history()
