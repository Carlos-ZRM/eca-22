"""Example of object creation and usage.
ECA evolutions.
"""

import ca_class

eca = ca_class.Eca(rule_number=22)
eca.define_evolution_config(
    size=50, evolutions=50, print_method="pyplot", init_method="single_cell"
)
eca.evolution()
eca.print_history()
