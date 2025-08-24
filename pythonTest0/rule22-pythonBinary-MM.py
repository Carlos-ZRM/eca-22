# -*- coding: utf-8 -*-
"""
This program demonstrates binary array manipulation, with optional
GPU acceleration, and now saves the final result to a MongoDB database
using an efficient and scalable storage pattern. It also includes
a function to apply morphological erosion to the output image.
"""
import numpy as np
import time
from datetime import datetime

# --- Image Saving Libraries (CPU-based) ---
from PIL import Image

# --- Attempt to import CuPy for GPU acceleration ---
try:
    import cupy as cp
    GPU_AVAILABLE = True
    print("CuPy found. GPU acceleration is available.")
except ImportError:
    GPU_AVAILABLE = False
    print("CuPy not found. Running on CPU with NumPy.")

# --- Attempt to import PyMongo for MongoDB storage ---
try:
    import pymongo
    from pymongo.binary import Binary
    MONGO_AVAILABLE = True
    print("PyMongo found. MongoDB functionality is available.")
except ImportError:
    MONGO_AVAILABLE = False
    print("PyMongo not found. MongoDB functionality is disabled.")

# --- Attempt to import OpenCV for image processing ---
try:
    import cv2 as cv
    CV_AVAILABLE = True
    print("OpenCV found. Image processing functionality is available.")
except ImportError:
    CV_AVAILABLE = False
    print("OpenCV not found. Image processing functionality is disabled.")

# Define json template object for CA
"""
json_template = {
    "id": "<CA_ID>",
    "description": "<CA_DESCRIPTION>",
    "rules": int(<CA_RULES>),
    "init_type": str(<CA_INIT_TYPE> | one_of(["random", "seed", "middle"])),
    "initial_state": np.ndarray,
    "array_size": int(<CA_ARRAY_SIZE>),
    "num_evolutions": int(<CA_EVOLUTIONS>),
    "array_history": list[np.ndarray],
    "fractal": bool(<CA_FRACTAL>),
    "fractal_dimension": float(<CA_FRACTAL_DIMENSION>)
}
"""


def init(N, use_gpu=False):
    """Initializes the binary array with a single '1' in the middle.

    Args:
        N (int): The size of the array.
        use_gpu (bool): Flag indicating whether to use GPU acceleration.
    Returns:
        numpy.ndarray: The initialized binary array.
    """
    xp = cp if use_gpu and GPU_AVAILABLE else np
    # Generate A vector with zeros
    A = xp.zeros(N, dtype=np.uint8)

    middle_index = N // 2
    A[middle_index] = 1
    return A

def init_seed(N, seed, use_gpu=False):
    """Initializes the binary array with a random seed.

    Args:
        N (int): The size of the array.
        seed (string): The String seed.
        use_gpu (bool): Flag indicating whether to use GPU acceleration.

    Returns:
        numpy.ndarray: The initialized binary array.
    """
    xp = cp if use_gpu and GPU_AVAILABLE else np
    # Generate A vector with zeros
    A = xp.zeros(N, dtype=np.uint8)

    A[xp.random.randint(0, N)] = 1
    return A

def init_random(N, rdensity, use_gpu=False):
    """Creates a random array on either the CPU (NumPy) or GPU (CuPy)."""
    xp = cp if use_gpu and GPU_AVAILABLE else np
    random_values = xp.random.rand(N)
    return (random_values < rdensity).astype(np.uint8)


def next_evolution(A, use_gpu=False):
    """Performs one evolution step on either a NumPy or CuPy array."""
    xp = cp if use_gpu and GPU_AVAILABLE else np

    # Create array 'B' by shifting 'A' one position to the left.
    B = np.concatenate((A[1:], [A[0]]))

    # Create array 'C' by shifting 'A' one position to the right.
    C = np.concatenate(([A[-1]], A[:-1]))

    return (A ^ B ^ C) ^ (A & B & C)
    ## Regla 30

def evolution(start_array, steps, use_gpu=False):
    """Evolves a starting array for a given number of steps on CPU or GPU."""
    A = start_array.copy()
    history = [A]
    for _ in range(steps):
        A = next_evolution(A, use_gpu)
        history.append(A)
    return history


def create_image_with_pillow(data, filename="evolution.png"):
    """Efficiently converts data (from CPU) to an image using Pillow."""
    print(f"\nCreating image with Pillow and saving as '{filename}'...")
    image_data = np.array(data)
    scaled_data = (image_data * 255).astype(np.uint8)
    image = Image.fromarray(scaled_data, mode='L')

    image.save(filename)
    print("Image saved successfully.")


def apply_erosion(image_path):
    """
    Applies morphological erosion to a saved image using two different kernels.
    """
    if not CV_AVAILABLE:
        print("\nOpenCV is not installed. Skipping erosion.")
        return

    print(f"\nApplying morphological erosion to '{image_path}'...")
    try:
        # Read the image in grayscale mode (0)
        img = cv.imread(image_path, 0)
        if img is None:
            print(f"Error: Could not read the image file at '{image_path}'.")
            return

        # Define the two kernels
        kernel_5x5 = np.array([[0,1,0],
                               [1,1,1]], np.uint8)
        kernel_custom = np.array([
                                  [0, 0, 0, 1, 0, 0, 0 ],
                                  [0, 0, 1, 1, 1, 0, 0 ],
                                  [0, 1, 0, 0, 0, 1 , 0],
                                  [1, 1, 1, 0, 1, 1 , 1]], np.uint8)

        # Apply erosion with each kernel
        dilation_5x5 = cv.dilate(img, kernel_5x5, iterations=7)
        dilation_custom = cv.dilate(img, kernel_custom, iterations=3)

        erosion_custom = cv.morphologyEx(img, cv.MORPH_OPEN, kernel_custom, iterations=1)
        gradiation_custom = cv.morphologyEx(img, cv.MORPH_GRADIENT, kernel_custom, iterations=5)
        black_hat_custom = cv.morphologyEx(img, cv.MORPH_BLACKHAT, kernel_custom, iterations=5)


        # Save the results
        filename_5x5 = "dilated_image_5x5.png"
        filename_dilation = "dilated_image_custom.png"
        filename_erosion = "eroded_image_custom.png"
        filename_gradient = "gradient_image_custom.png"
        filename_black_hat = "black_hat_image_custom.png"


        cv.imwrite(filename_5x5, dilation_5x5, [cv.IMWRITE_PNG_BILEVEL, 1])
        cv.imwrite(filename_dilation, dilation_custom, [cv.IMWRITE_PNG_BILEVEL, 1])
        cv.imwrite(filename_erosion, erosion_custom, [cv.IMWRITE_PNG_BILEVEL, 1])
        cv.imwrite(filename_gradient, gradiation_custom, [cv.IMWRITE_PNG_BILEVEL, 1])
        cv.imwrite(filename_black_hat, black_hat_custom, [cv.IMWRITE_PNG_BILEVEL, 1])

        print(f"Saved erosion with 5x5 kernel to '{filename_5x5}'")
        print(f"Saved erosion with custom kernel to '{filename_custom}'")

    except Exception as e:
        print(f"An error occurred during erosion: {e}")


def save_to_mongodb_efficient(history, params):
    """
    Saves the evolution history efficiently to MongoDB using two collections.
    """
    if not MONGO_AVAILABLE:
        print("\nPyMongo is not installed. Skipping MongoDB save.")
        return

    print(f"\nSaving evolution history to MongoDB (Efficient Method)...")

    connection_string = "mongodb://localhost:27017/"

    try:
        client = pymongo.MongoClient(connection_string)
        db = client["automata_db"]
        metadata_collection = db["runs_metadata"]
        steps_collection = db["evolution_steps"]

        run_id = f"run_{int(time.time())}"
        metadata_doc = {"_id": run_id, "timestamp": datetime.utcnow(), "parameters": params}
        metadata_collection.insert_one(metadata_doc)
        print(f"Inserted metadata for run_id: {run_id}")

        step_documents = []
        for i, step_array in enumerate(history):
            vector_binary = Binary(step_array.astype(np.uint8).tobytes())
            doc = {
                "run_id": run_id,
                "step": i,
                "vector": vector_binary,
                "isFractal": "" # Fixed missing comma from previous version
            }
            step_documents.append(doc)

        if step_documents:
            steps_collection.insert_many(step_documents)
            print(f"Successfully inserted {len(step_documents)} step documents.")
            print("\nPro Tip: For fast queries, create an index in the mongo shell:")
            print(f'db.evolution_steps.createIndex({{ "run_id": 1, "step": 1 }})')

    except pymongo.errors.ConnectionFailure as e:
        print(f"Error: Could not connect to MongoDB at '{connection_string}'.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    params = {"steps": 5000, "N": 10001, "rdensity": 0.045}
    #params = {"steps": 50000, "N": 50000, "rdensity": 0.00045}

    print("\nRunning evolution on CPU.")
    start_time = time.time()

    # Correctly initialize the state
    initial_state = init_random(params["N"], params["rdensity"], use_gpu=False)
    #initial_state = init(params["N"], use_gpu=False)  # Fallback to the original init if needed
    evolution_history_cpu = evolution(initial_state, params["steps"], use_gpu=False)

    end_time = time.time()
    print(f"Data generation took: {end_time - start_time:.4f} seconds")

    output_image_filename = "evolution_cpu_generated.png"
    create_image_with_pillow(evolution_history_cpu, filename=output_image_filename)

    # Apply the new erosion function to the generated image
    apply_erosion(output_image_filename)

    # Save the final history to MongoDB
    save_to_mongodb_efficient(evolution_history_cpu, params)
