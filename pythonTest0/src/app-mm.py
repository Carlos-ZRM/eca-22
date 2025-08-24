
import ca_mm_object

"""
Example of object creation and usage.
ECA object and applied all morphological operations.
"""
eca = ca_mm_object.ECA_MM(rule_number=22)
eca.define_evolution_config(size=500, evolutions=500, print_method="png")
eca.evolution()
eca.dilation()
eca.erosion()
eca.gradation()
eca.black_hat()
eca.print_history()
