class AppSettings:
    """
    A class to hold static configuration variables for the application.
    This helps in organizing default settings and constants in one place.
    """

    # Define the list of rules as a static class variable.
    CELLULAR_AUTOMATA_RULES = [
        "18",
        "22",
        "30",
        "54",
        "60",
        "90",
        "110",
    ]
    CELLULAR_AUTOMATA_INIT_METHODS = [
        "single_cell",
        "random",
    ]
    CELLULAR_AUTOMATA_PRINT_METHODS = [
        "png"
    ]

class MorphologySettings:
    """
    A class to hold static configuration variables for the morphology application.
    This helps in organizing default settings and constants in one place.
    """
    import numpy as np


    KERNEL_SMALL = np.array([[0, 1, 0], [1, 1, 1]], np.uint8)
    KERNEL_LARGE = np.array([[0, 0, 1, 0, 0], [0, 1, 1, 1, 0], [1, 1, 1, 1, 1]], np.uint8)

    KERNEL_OPTIONS = {
        "small": KERNEL_SMALL,
        "large": KERNEL_LARGE,
    }

    # Define the list of morphology operations as a static class variable.
    MORPHOLOGY_OPERATIONS = [
        "dilation",
        "erosion",
        "gradation",
        "blackhat",
    ]

