import numpy as np
import matplotlib.pyplot as plt
import time
from PIL import Image

class ECA:
    dict_rules = {
        18: lambda P, Q, R: (~Q) & (P ^ R),
        22: lambda P, Q, R: (P ^ Q ^ R) ^ (P & Q & R),
        26: lambda P, Q, R: P ^ ( R | (P & Q)),
        30: lambda P, Q, R: P ^ ( Q | R),
        60: lambda P, Q, R: P ^ Q,
        90: lambda P, Q, R: P ^ R,
        94: lambda P, Q, R: (Q & ~P) | (P ^ R),
        105: lambda P, Q, R: ~ ( P ^ Q ^ R),
        106: lambda P, Q, R: R ^ ( P & Q),
        122: lambda P, Q, R: ( P & ~ Q) | ( Q ^ R),
        133: lambda P, Q, R: (~(P ^ R)) & (Q | (~ P)),
        126: lambda P, Q, R: ( P ^ Q ) | ( P ^ R),
        146: lambda P, Q, R: (P | Q) & (P ^ Q ^ R),
        150: lambda P, Q, R: P ^ Q ^ R,
        154: lambda P, Q, R: R ^ ( P & ~Q),
        164: lambda P, Q, R: P ^ R ^ ( P | Q | R)
        # Add more rules as needed, e.g.:
        # 90: lambda P, Q, R: A ^ C,
    }

    def __init__(self, rule_number=22):
        self.rule_number = rule_number

    def define_evolution_config(self, size, evolutions, init_method="single_cell", print_method="pyplot"):
        """ Initialize evolution configuration parameters
        Args:
            size (int): Size of the cellular automa array.
            evolutions (int): Number of desired evolutions.
            init_method (string): Initialization method for the cellular automaton.
            print_method (string): Method to print or visualize the automaton.
        Returns:
            None
        """
        self.size = size
        self.evolutions = evolutions
        self.history = []
        self.init_method = init_method
        self.print_method = print_method
        if init_method == "single_cell":
            self.init_state = self.init_one()

    def init_one(self):
        """
        Initialize the cellular automaton with a single active cell.

        Returns:
            np.ndarray: Initial state array with a single active cell.
        """
        init_state = np.zeros(self.size, dtype=np.uint8)
        init_state[self.size // 2] = 1
        return init_state

    def next_evolution(self, array):
        """
        Computes the next state of the cellular automaton.
        Make array 'A' by shifting 'B' one position to the left.
        Uses the rule defined in dict_rules to compute the next state.
        Args:
            array (np.ndarray): Current state array.
        Returns:
            np.ndarray: Next state array after applying the rule.
        """
        # Create array 'B' by shifting 'A' one position to the left.
        R = np.concatenate((array[1:], [array[0]]))
        # Create array 'C' by shifting 'A' one position to the right.
        P = np.concatenate(([array[-1]], array[:-1]))
        return self.dict_rules[self.rule_number](P, array, R)

    def evolution(self, start_array=None):
        """
        Evolves the cellular automaton for a specified number of generations (defined by self.evolutions).
        start_array (numpy.ndarray): The initial state of the cellular automaton.

        Args:
            start_array (np.ndarray): Initial state array.
            steps (int): Number of evolution steps.
        Returns:
            list: List of np.ndarray representing the history of states.
        """
        # Measure the initial time
        initial_time = time.time()
        # If start_array is None, use the initial state
        if start_array is None:
            start_array = self.init_state
        # Create history list (matrix)
        self.history = [start_array]
        # Create current array
        current_array = start_array
        # Iterate through the specified number of evolutions
        for _ in range(self.evolutions):
            current_array = self.next_evolution(current_array)
            self.history.append(current_array)
        # Measure the final time
        final_time = time.time()
        print(f"Evolution execution time: {final_time - initial_time:.6f} seconds")
        return self.history
    
    def print_history(self):
        """
        Prints the history of states in the cellular automaton.
        """
        if self.print_method == "pyplot":
            self.__print_pyplot()
        elif self.print_method == "png":
                self._print_img()
        else:
            for step in self.history:
                print(step)

    def __print_pyplot(self):
        """
        Visualizes the history of states in the cellular automaton using matplotlib.
        """
        plt.imshow(self.history, cmap='binary', aspect='auto')
        plt.title(f'Evolution of Rule {self.rule_number}')
        plt.show()
    
    def _print_img(self):
        file_name = f"CA_history_rule_{self.rule_number}.png"
        image_data = np.array(self.history)
        scaled_data = (image_data * 255).astype(np.uint8)
        image = Image.fromarray(scaled_data, mode='L')
        image.save(file_name)
        return file_name


