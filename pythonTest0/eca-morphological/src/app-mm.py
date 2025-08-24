import CA_MM_Object

"""
Example of object creation and usage.
ECA object and applied all morphological operations.
"""
eca = CA_MM_Object.ECA_MM(rule_number=22)
eca.define_evolution_config(size=500, evolutions=500, print_method="png")
eca.evolution()
eca.dilation()
eca.erosion()
eca.gradation()
eca.black_hat()
eca.print_history()
