# -*- coding: utf-8 -*-
"""
This program demonstrates binary array manipulation, with optional
GPU acceleration, and now saves the final result to a MongoDB database
using an efficient and scalable storage pattern.
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


def init_random(N, rdensity, use_gpu=False):
    """Creates a random array on either the CPU (NumPy) or GPU (CuPy)."""
    xp = cp if use_gpu and GPU_AVAILABLE else np
    random_values = xp.random.rand(N)
    return (random_values < rdensity).astype(int)


def next_evolution(A, use_gpu=False):
    """Performs one evolution step on either a NumPy or CuPy array."""
    xp = cp if use_gpu and GPU_AVAILABLE else np
    
    B = xp.concatenate((A[1:], xp.array([0])))
    C = xp.concatenate((xp.array([0]), A[:-1]))
    
    return (A ^ B ^ C) ^ (A & B & C)


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


def save_to_mongodb_efficient(history, params):
    """
    Saves the evolution history efficiently to MongoDB using two collections:
    1. 'runs_metadata': One document per run with the parameters.
    2. 'evolution_steps': One document per step, storing vector data as compact binary.
    """
    if not MONGO_AVAILABLE:
        print("\nPyMongo is not installed. Skipping MongoDB save.")
        return

    print(f"\nSaving evolution history to MongoDB (Efficient Method)...")
    
    connection_string = "mongodb://localhost:27017/"
    
    try:
        client = pymongo.MongoClient(connection_string)
        db = client["automata_db"]
        
        # Define collections
        metadata_collection = db["runs_metadata"]
        steps_collection = db["evolution_steps"]
        
        # 1. Create a single metadata document for the entire run
        run_id = f"run_{int(time.time())}"
        metadata_doc = {
            "_id": run_id,
            "timestamp": datetime.utcnow(),
            "parameters": params
        }
        metadata_collection.insert_one(metadata_doc)
        print(f"Inserted metadata for run_id: {run_id}")

        # 2. Prepare step documents for batch insertion
        step_documents = []
        for i, step_array in enumerate(history):
            # Convert array to compact binary format
            vector_binary = Binary(step_array.astype(np.uint8).tobytes())
            doc = {
                "run_id": run_id, # Link back to the metadata
                "step": i,
                "vector": vector_binary
                "isFractal": ""
                
            }
            step_documents.append(doc)

        # 3. Insert all step documents in a single, efficient batch operation
        if step_documents:
            steps_collection.insert_many(step_documents)
            print(f"Successfully inserted {len(step_documents)} step documents.")
            print("\nPro Tip: For fast queries, create an index in the mongo shell:")
            print(f'db.evolution_steps.createIndex({{ "run_id": 1, "step": 1 }})')

    except pymongo.errors.ConnectionFailure as e:
        print(f"Error: Could not connect to MongoDB at '{connection_string}'.")
        print("Please ensure MongoDB is running and the connection string is correct.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    # --- Parameters ---
    params = {
        "steps": 500,
        "N": 1001,
        "rdensity": 0.5
    }
    
    # --- Execution ---
    print("\nRunning evolution on CPU.")
    start_time = time.time()

    initial_state = init_random(params["N"], params["rdensity"], use_gpu=False)
    evolution_history_cpu = evolution(initial_state, params["steps"], use_gpu=False)

    end_time = time.time()
    print(f"Data generation took: {end_time - start_time:.4f} seconds")

    create_image_with_pillow(evolution_history_cpu, filename="evolution_cpu_generated.png")
    
    # Save the final history to MongoDB using the new efficient method
    save_to_mongodb_efficient(evolution_history_cpu, params)

