"""ECA class for elementary cellular automata."""

import time

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


class Eca:
    """ECA class for elementary cellular automata."""

    dict_rules = {
        18: lambda P, Q, R: (~Q) & (P ^ R),
        22: lambda P, Q, R: (P ^ Q ^ R) ^ (P & Q & R),
        26: lambda P, Q, R: P ^ (R | (P & Q)),
        30: lambda P, Q, R: P ^ (Q | R),
        54: lambda P, Q, R:  Q ^ (P | R),
        60: lambda P, Q, R: P ^ Q,
        90: lambda P, Q, R: P ^ R,
        94: lambda P, Q, R: (Q & ~P) | (P ^ R),
        105: lambda P, Q, R: ~(P ^ Q ^ R),
        110: lambda P, Q, R: (Q & ~P) | (Q ^ R),
        106: lambda P, Q, R: R ^ (P & Q),
        122: lambda P, Q, R: (P & ~Q) | (Q ^ R),
        133: lambda P, Q, R: (~(P ^ R)) & (Q | (~P)),
        126: lambda P, Q, R: (P ^ Q) | (P ^ R),
        146: lambda P, Q, R: (P | Q) & (P ^ Q ^ R),
        150: lambda P, Q, R: P ^ Q ^ R,
        154: lambda P, Q, R: R ^ (P & ~Q),
        164: lambda P, Q, R: P ^ R ^ (P | Q | R),
        195: lambda P, Q, R: ~(P ^ Q),
        # Add more rules as needed, e.g.:
        # 90: lambda P, Q, R: A ^ C,
    }

    def set_pixel_size(self, pixel_size):
        self.pixel_size = pixel_size

    def get_pixel_size(self):
        return self.pixel_size
    
    def __init__(self, rule_number=22):
        self.rule_number = rule_number
        self.size = None
        self.evolutions = None
        self.history = None
        self.init_method = None
        self.print_method = None
        self.init_state = None
        self.seed = None
        self.cell_color_1 = 0 
        self.pixel_size = 1
         # default color black

    def define_evolution_config(
        self,
        size,
        evolutions,
        init_method="single_cell",
        print_method="pyplot",
        seed="01011001010",
    ):
        """Initialize evolution configuration parameters
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
        # Initialize the state based on the chosen method
        if init_method == "single_cell":
            self.init_state = self.init_one()
        elif init_method == "single_cell_zero":
            self.init_state = self.init_zero()
        elif init_method == "random":
            self.init_state = self.init_random()
        elif init_method == "seed":
            self.seed = seed
            self.init_state = self.init_seed(seed)
        elif init_method == "seed_zero":
            self.seed = seed
            self.init_state = self.init_seed_zero(seed)

    def init_one(self):
        """Initialize the cellular automaton with a single active cell.

        Returns:
            np.ndarray: Initial state array with a single active cell.

        """
        init_state = np.zeros(self.size, dtype=np.uint8)

        init_state[0] = 1
        # init_state[self.size // 2] = 1

        return init_state

    def init_zero(self):
        """Initialize the cellular automaton with all cells inactive.

        Returns:
            np.ndarray: Initial state array with all cells inactive.

        """
        init_state = np.ones(self.size, dtype=np.uint8)
        init_state[self.size // 2] = 0
        print(init_state)
        return init_state

    def init_random(self, rdensity=0.5):
        """Initialize the cellular automaton with a random state.

        Args:
            rdensity (float): Density of random 1s in the initial state.

        Returns:
            np.ndarray: Initial state array with random values.

        """
        #return np.random.choice([0, 1], size=self.size, p=[rdensity, 1 - rdensity])
        return (np.random.random(self.size) < rdensity).astype(int)
    
    def init_seed(self, seed):
        """Initialize the cellular automaton with a seed string.

        Args:
            seed (str): A string of 0s and 1s representing the initial state.

        Returns:
            np.ndarray: Initial state array based on the seed string.

        """
        # Define the position to insert the seed
        pos = (self.size - len(seed)) // 2
        # Create the initial state array
        init_state = np.zeros(self.size, dtype=np.uint8)
        # create seed array
        seed_array = np.fromstring(seed, dtype=np.uint8) - ord("0")
        # insert seed array into initial state
        init_state[pos : pos + len(seed)] = seed_array
        return init_state

    def init_seed_zero(self, seed):
        """Initialize the cellular automaton with a seed string.

        Args:
            seed (str): A string of 0s and 1s representing the initial state.

        Returns:
            np.ndarray: Initial state array based on the seed string.

        """
        # Define the position to insert the seed
        pos = (self.size - len(seed)) // 2
        # Create the initial state array
        init_state = np.ones(self.size, dtype=np.uint8)
        # create seed array
        seed_array = np.fromstring(seed, dtype=np.uint8) - ord("0")
        # insert seed array into initial state
        init_state[pos : pos + len(seed)] = seed_array
        print(init_state)
        return init_state

    def next_evolution(self, array):
        """Computes the next state of the cellular automaton.
        Make array 'A' by shifting 'B' one position to the left.
        Uses the rule defined in dict_rules to compute the next state.

        Args:
            array (np.ndarray): Current state array.

        Returns:
            np.ndarray: Next state array after applying the rule.

        """
        # Create array 'B' by shifting 'A' one position to the left.
        r = np.concatenate((array[1:], [array[0]]))
        # Create array 'C' by shifting 'A' one position to the right.
        p = np.concatenate(([array[-1]], array[:-1]))
        return self.dict_rules[self.rule_number](p, array, r)

    def evolution(self, start_array=None):
        """Evolves the cellular automaton for a specified
        number of generations (defined by self.evolutions).
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
        """Prints the history of states in the cellular automaton."""
        if self.print_method == "pyplot":
            return self.__print_pyplot()
        elif self.print_method == "png":
            return self._print_img()
        elif self.print_method == "png_file":
            return self._print_img(save_file=True)
        else:
            for step in self.history:
                print(step)

    def __print_pyplot(self):
        """Visualizes the history of states in the cellular automaton using matplotlib."""
        plt.imshow(self.history, cmap="binary", aspect="auto")
        plt.title(f"Evolution of Rule {self.rule_number}")
        plt.show()

    def _print_img(self,save_file=False):
        file_name = f"CA_history_rule_{self.rule_number}.png"
        image_data = np.array(self.history)
        if self.cell_color_1 == 0:
            # Invert colors: 1 becomes black (0), 0 becomes white (255)
            scaled_data = ((1 - image_data) * 255).astype(np.uint8)
        else:
            scaled_data = (image_data * 255).astype(np.uint8)
        image = Image.fromarray(scaled_data, mode="L")
        print(f"Image generated: {file_name}")
        if save_file:
            self.image_file = file_name
            image.save(file_name)
        return image

def to_string(obj):
    """
    Returns a string representation of an object, showing all its
    instance variables and their values.

    Args:
        obj: The object to convert to a string.

    Returns:
        A formatted string with the object's class name and its attributes.
    """
    # Get the class name of the object
    class_name = obj.__class__.__name__

    # Get the dictionary of instance variables
    attributes = vars(obj)

    # Format the attributes into a readable string
    attr_list = [f"{key}={repr(value)}" for key, value in attributes.items()]
    attrs_str = ", ".join(attr_list)

    # Combine the class name and attributes
    return f"{class_name}({attrs_str})"
