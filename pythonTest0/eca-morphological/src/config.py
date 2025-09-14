class AppSettings:
    """
    A class to hold static configuration variables for the application.
    This helps in organizing default settings and constants in one place.
    """

    # Define the list of rules as a static class variable.
    CELLULAR_AUTOMATA_RULES = [
        "18",
        "22",
    ]
    CELLULAR_AUTOMATA_INIT_METHODS = [
        "Single Cell",
        "Random",
        "Seeds",
    ]
    CELLULAR_AUTOMATA_PRINT_METHODS = [
        "Pyplot",
        "PIL",
    ]
