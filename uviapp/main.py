import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from PIL import Image, ImageDraw, ImageFont

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../pythonTest0/eca-morphological/src')))
import ca_class
import io
import base64

# --- Application Setup ---
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Python variable for the rule list
CELLULAR_AUTOMATA_RULES = [
    "Rule 30",
    "Rule 90",
    "Rule 110",
    "Rule 184 (Traffic)",
    "Seeds",
    "Life (Conway)",
]

# --- Pydantic Model for Input Validation ---
class SimulationParams(BaseModel):
    rule: str
    cell_space: int
    num_evolutions: int

# --- API Endpoints ---

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serves the main HTML page and passes the rule list to it."""
    return templates.TemplateResponse(
        "index.html", {"request": request, "rules": CELLULAR_AUTOMATA_RULES}
    )

@app.post("/generate_image")
async def generate_image(params: SimulationParams):
    """
    Receives parameters, generates a placeholder image with the data written on it,
    and returns it as a Base64-encoded data URL.
    """
    eca_rule_number = params.rule
    eca_size = params.cell_space
    eca_evolutions = params.num_evolutions
    eca = ca_class.Eca(rule_number=eca_rule_number)
    eca.define_evolution_config(
        size=eca_size, evolutions=eca_evolutions, print_method="pyplot", init_method="single_cell"
    )
    
    width, height = 400, 400
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", 15)
    except IOError:
        font = ImageFont.load_default()

    # Draw the received parameters onto the image
    draw.text((10, 10), "Image Generated with Parameters:", fill='black', font=font)
    draw.text((20, 40), f"- Rule: {params.rule}", fill='black', font=font)
    draw.text((20, 60), f"- Cell Space: {params.cell_space}", fill='black', font=font)
    draw.text((20, 80), f"- Evolutions: {params.num_evolutions}", fill='black', font=font)
    draw.rectangle([0, 0, width-1, height-1], outline="black", width=2)

    # Save image to a memory buffer
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    
    # Encode the image to Base64 and create a data URL
    img_str = base64.b64encode(buffered.getvalue()).decode()
    img_data_url = f"data:image/png;base64,{img_str}"

    return {"image_data": img_data_url}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
