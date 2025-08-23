import CA_Object

eca = CA_Object.ECA(rule_number=22)
eca.define_evolution_config(size=500, evolutions=500,print_method="png")
eca.evolution()
eca.print_history()