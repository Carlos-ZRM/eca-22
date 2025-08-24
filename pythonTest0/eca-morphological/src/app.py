"""Example of object creation and usage.
ECA evolutions.
"""

import ca_object

eca = ca_object.Eca(rule_number=22)
eca.define_evolution_config(
    size=500, evolutions=500, print_method="pyplot", init_method="seed_zero"
)
eca.evolution()
eca.print_history()
