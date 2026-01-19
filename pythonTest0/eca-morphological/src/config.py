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
