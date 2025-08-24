import CA_Object

eca = CA_Object.ECA(rule_number=22)
eca.define_evolution_config(size=500, evolutions=500,print_method="pyplot",init_method="seed_zero")
eca.evolution()
eca.print_history()
