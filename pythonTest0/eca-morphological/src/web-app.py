import io
import base64
import ca_class

import cv2
import numpy as np
import uvicorn

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from PIL import Image, ImageDraw, ImageFont


# Import the settings class from your new config file
from config import AppSettings, MorphologySettings

# --- Application Setup ---
app = FastAPI()
# Assume the templates directory is relative to the project root
templates = Jinja2Templates(directory="templates")

# Mount static files (CSS, JS, images, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")


# --- Pydantic Models for Input Validation ---
class MorphologicalParams(BaseModel):
    image_data: str       # base64 data URL from canvas
    operation: str        # dilation | erosion | gradation | blackhat
    kernel: str           # small | large
    iterations: int = 1
    pixel_size: int = 1


class SimulationParams(BaseModel):
    rule: str
    cell_space: int
    num_evolutions: int
    init_method: str
    print_method: str
    density: float = 0.5
    pixel_size: int = 3
      # Default pixel size value


# --- API Endpoints ---


@app.get("/debug", response_class=HTMLResponse)
async def debug_page(request: Request):
    """Debug page to check if backend data is being passed correctly."""
    return templates.TemplateResponse(
        "debug.html",
        {
            "request": request,
            "rules": AppSettings.CELLULAR_AUTOMATA_RULES,
            "init_methods": AppSettings.CELLULAR_AUTOMATA_INIT_METHODS,
            "print_methods": AppSettings.CELLULAR_AUTOMATA_PRINT_METHODS,
        },
    )


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serves the main HTML page and passes the config lists from the AppSettings class."""
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "rules": AppSettings.CELLULAR_AUTOMATA_RULES,
            "init_methods": AppSettings.CELLULAR_AUTOMATA_INIT_METHODS,
            "print_methods": AppSettings.CELLULAR_AUTOMATA_PRINT_METHODS,
            "morphology_operations": MorphologySettings.MORPHOLOGY_OPERATIONS,
            "kernel_options": list(MorphologySettings.KERNEL_OPTIONS.keys()),
        },
    )


@app.post("/generate_image")
async def generate_image(params: SimulationParams):
    """
    Receives parameters, generates a CA evolution image,
    and returns it as a Base64-encoded data URL.
    """
    eca_rule_number = int(params.rule)
    eca_size = int(params.cell_space)
    eca_evolutions = int(params.num_evolutions)
    eca_init_method = params.init_method
    eca_print_method = params.print_method
    eca_density = float(params.density)
    eca = ca_class.Eca(rule_number=eca_rule_number)
    eca.define_evolution_config(
        size=eca_size, 
        evolutions=eca_evolutions, 
        print_method=eca_print_method, 
        init_method=eca_init_method
    )
    
    # If using random init method, pass the density to the init_random method
    # This requires modifying the evolution method to accept density parameter
    if eca_init_method == "random":
        eca.init_state = eca.init_random(rdensity=eca_density)
    
    eca.evolution()

    pixel_size = max(1, min(15, params.pixel_size))

    # Generate raw image (pixel_size=1) — used as input for morphological ops
    eca.set_pixel_size(1)
    img_raw = eca.print_history()

    # Scale for display
    if pixel_size > 1:
        img_display = img_raw.resize(
            (img_raw.width * pixel_size, img_raw.height * pixel_size), Image.NEAREST
        )
    else:
        img_display = img_raw

    def to_data_url(img):
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

    return {
        "image_data": to_data_url(img_display),
        "raw_image_data": to_data_url(img_raw),
    }

@app.post("/generate_morphological")
async def generate_morphological(params: MorphologicalParams):
    """
    Receives a base64 canvas image and morphological parameters,
    applies the selected operation via OpenCV, and returns the result
    as a Base64-encoded data URL.
    """
    # Decode base64 image from canvas
    header, encoded = params.image_data.split(",", 1)
    img_bytes = base64.b64decode(encoded)
    np_arr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_GRAYSCALE)

    print("Morphological operation:", params.operation)
    kernel = MorphologySettings.KERNEL_OPTIONS.get(params.kernel, MorphologySettings.KERNEL_SMALL)
    iterations = max(1, params.iterations)
    pixel_size = max(1, min(15, params.pixel_size))

    if params.operation == "dilation":
        result = cv2.dilate(img, kernel, iterations=iterations)
    elif params.operation == "erosion":
        result = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel, iterations=iterations)
    elif params.operation == "gradation":
        result = cv2.morphologyEx(img, cv2.MORPH_GRADIENT, kernel, iterations=iterations)
    elif params.operation == "blackhat":
        result = cv2.morphologyEx(img, cv2.MORPH_BLACKHAT, kernel, iterations=iterations)
    else:
        result = img

    # raw result (pixel_size=1) — sent back so the client can chain operations correctly
    raw_pil = Image.fromarray(result)

    # scaled result for display
    if pixel_size > 1:
        display_pil = raw_pil.resize(
            (raw_pil.width * pixel_size, raw_pil.height * pixel_size), Image.NEAREST
        )
    else:
        display_pil = raw_pil

    def to_data_url(img):
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

    return {
        "image_data": to_data_url(display_pil),
        "raw_image_data": to_data_url(raw_pil),
    }


if __name__ == "__main__":
    # Run options (both include timestamps via log_config.json):
    #   python web-app.py
    #   uvicorn web-app:app --reload --log-config log_config.json
    uvicorn.run(app, host="127.0.0.1", port=8000, log_config="log_config.json")