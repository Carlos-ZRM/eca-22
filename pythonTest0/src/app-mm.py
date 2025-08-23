import CA_MM_Object

eca = CA_MM_Object.ECA_MM(rule_number=22)
eca.define_evolution_config(size=500, evolutions=500, print_method="png")
eca.evolution()
eca.dilation()
eca.erosion()
eca.gradation()
eca.black_hat()
eca.print_history()