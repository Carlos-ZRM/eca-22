# -*- coding: utf-8 -*-
"""
This program demonstrates binary array manipulation using the NumPy library,
including initialization, bit shifting, and a complex logical operation.
It now saves the evolution history and generates an image from it.
"""
# We import the numpy library, commonly aliased as np.
# This is the standard for numerical and array operations in Python.
import numpy as np
# We import the Image class from the PIL (Pillow) library for image creation.
from PIL import Image
# Pillow is a fork of the original PIL (Python Imaging Library) and is used for image
# processing tasks such as creating, manipulating, and saving images.
# We import matplotlib to create an image from the array data.
import matplotlib.pyplot as plt

def print_array_as_string(name, array):
  """Helper function to print the array in a clean binary string format."""
  # Converts each integer in the list to a string and joins them together.
  array_str = "".join(map(str, array))
  print(f"{name}: {array_str}")

def init(N):
    """Initializes the binary array with a single '1' in the middle."""
    A = np.zeros(N, dtype=int)
    middle_index = N // 2
    A[middle_index] = 1
    return A

def init_random(N, rdensity):
    """
    Creates a NumPy array Z of size N with 1s set randomly based on rdensity.
    """
    # Generate an array of N random floats between 0.0 and 1.0.
    random_values = np.random.rand(N)
    # Where the random value is less than rdensity, the result is True (1),
    # otherwise it is False (0). Convert the boolean array to integers.
    Z = (random_values < rdensity).astype(int)
    return Z

def next_evolution(A):
    print(("\n" + "-" * 50 + "\n"
           "Performing evolution step...\n" + "-" * 50))
    print_array_as_string("Current State A", A)
    print("Shifting A to create B and C...")
    """Performs the evolution of the binary array."""
    # Create array 'B' by shifting 'A' one position to the left.
    B = np.concatenate((A[1:], [A[0]]))

    # Create array 'C' by shifting 'A' one position to the right.
    C = np.concatenate(([A[-1]], A[:-1]))

    # Execute the operation: (A, B, C) ↦ A XOR B XOR C XOR (A AND B AND C)
    result_array = (A ^ B ^ C) ^ (A & B & C)
    print_array_as_string("Result State", result_array)
    return result_array

def evolution(start_array, steps):
    """
    Evolves a starting binary array for a given number of steps.
    """
    # The starting array is now passed in as a parameter.
    A = start_array.copy() # Use a copy to avoid modifying the original start array

    # Create a list to store the history of each evolution step.
    history = [A]

    # Iterate through the number of evolution steps.
    for step in range(steps):
        # Perform the evolution and update A.
        A = next_evolution(A)
        # Append the new state to our history.
        history.append(A)

    # Return the complete history of evolutions.
    return history

def create_image(data, filename="evolution_pattern.png"):
    """
    Converts the evolution data into an image using Matplotlib.
    """
    print(f"\nCreating image from data and saving as '{filename}'...")
    # Convert the list of arrays into a 2D NumPy array.
    image_data = np.array(data)

    plt.figure(figsize=(10, 10))
    # Use imshow to display the data as an image.
    # cmap='gray_r' makes 1s black and 0s white for better contrast.
    # interpolation='nearest' ensures pixels are sharp squares.
    plt.imshow(image_data, cmap='gray_r', interpolation='nearest')
    plt.title("Binary Array Evolution")
    plt.xlabel("Cell Position")
    plt.ylabel("Time Step")

    # Save the figure to a file.
    plt.savefig(filename)
    print("Image saved successfully.")


def create_image_with_pillow(data, filename="evolution_pillow.png"):
    """
    Converts the evolution data into an image using the Pillow library.
    This is much more efficient than using Matplotlib for raw image saving.
    """
    print(f"\nCreating image with Pillow and saving as '{filename}'...")

    # 1. Convert the list of arrays into a single 2D NumPy array.
    image_data = np.array(data)

    # 2. Scale the data to the 0-255 range for an 8-bit grayscale image.
    #    Our data is 0s and 1s. We map 0 -> 0 (black) and 1 -> 255 (white).
    #    The `astype(np.uint8)` is crucial as Pillow expects this data type.
    scaled_data = (image_data * 255).astype(np.uint8)

    # 3. Create an image from the NumPy array.
    #    The 'L' mode signifies an 8-bit grayscale image.
    image = Image.fromarray(scaled_data, mode='L')

    # 4. Save the image.
    image.save(filename)
    print("Image saved successfully with Pillow.")

if __name__ == "__main__":
    # Define the number of steps and the size of the binary array.
    steps = 5000 # Number of evolution steps to perform
    N = 5000

    # Define the random density for the initial state.
    # A value of 0.5 means each cell has a 50% chance of being 1.
    rdensity = 0.0002

    # Create the initial state using the new random function.
    # To use the old method, you could swap this line with:
    # initial_state = init(N)
    #initial_state = init_random(N, rdensity)
    initial_state = init(N)  # Ensure it's an integer array
    # Get the history of evolutions, starting from our initial state.
    evolution_history = evolution(initial_state, steps)

    # Print a few steps to the console for verification
    #print("--- Sample of Evolution (from random start) ---")
    #print_array_as_string(f"Step 0", evolution_history[0])
    #print_array_as_string(f"Step 1", evolution_history[1])
    #print_array_as_string(f"Step 2", evolution_history[2])

    # Create and save an image from the history.
    create_image(evolution_history, filename="evolution_random_start.png")
    # Create and save an image using Pillow for efficiency.
    #create_image_with_pillow(evolution_history, filename="evolution_random_start_pillow.png")
