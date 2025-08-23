import CA_Object

eca = CA_Object.ECA(rule_number=30)
eca.define_evolution_config(size=500, evolutions=500)
eca.evolution()
eca.print_history()