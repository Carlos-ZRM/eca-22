import numpy as np
import matplotlib.pyplot as plt
import time

class ECA:
    dict_rules = {
        30: lambda A, B, C: (A ^ B ^ C) ^ (A & B & C),
        # Add more rules as needed, e.g.:
        # 90: lambda A, B, C: A ^ C,
    }

    def __init__(self, rule_number=22):
        self.rule_number = rule_number

    def define_evolution_config(self, size, evolutions, init_method="single_cell", print_method="pyplot"):
        """ Initialize evolution configuration parameters

        size (int): Size of the cellular automa array.
        evolutions (int): Number of desired evolutions.
        init_method (string): Initialization method for the cellular automaton.

        """
        self.size = size
        self.evolutions = evolutions
        self.history = []
        self.init_method = init_method
        self.print_method = print_method
        if init_method == "single_cell":
            self.init_state = self.init_one()

    def init_one(self):
        # Initialize the cellular automaton with a single active cell
        init_state = np.zeros(self.size, dtype=np.uint8)
        init_state[self.size // 2] = 1
        return init_state

    def next_evolution(self, array):
        # Create array 'B' by shifting 'A' one position to the left.
        B = np.concatenate((array[1:], [array[0]]))
        # Create array 'C' by shifting 'A' one position to the right.
        C = np.concatenate(([array[-1]], array[:-1]))
        return self.dict_rules[self.rule_number](array, B, C)

    def evolution(self, start_array=None):
        initial_time = time.time()
        if start_array is None:
            start_array = self.init_state
        self.history = [start_array]
        current_array = start_array

        for _ in range(self.evolutions):
            current_array = self.next_evolution(current_array)
            self.history.append(current_array)
        final_time = time.time()
        print(f"Evolution execution time: {final_time - initial_time:.6f} seconds")
        return self.history
    def print_history(self):
        if self.print_method == "pyplot":
            plt.imshow(self.history, cmap='binary', aspect='auto')
            plt.title(f'Evolution of Rule {self.rule_number}')
            plt.show()
        else:
            for step in self.history:
                print(step)

