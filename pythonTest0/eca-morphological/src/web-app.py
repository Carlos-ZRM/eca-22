import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from PIL import Image, ImageDraw, ImageFont
import io
import base64

# Import the settings class from your new config file
from src.config import AppSettings

# --- Application Setup ---
app = FastAPI()
# Assume the templates directory is relative to the project root
templates = Jinja2Templates(directory="templates")


# --- Pydantic Model for Input Validation ---
class SimulationParams(BaseModel):
    rule: str
    cell_space: int
    num_evolutions: int
    init_method: str
    print_method: str


# --- API Endpoints ---


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
        },
    )


@app.post("/generate_image")
async def generate_image(params: SimulationParams):
    """
    Receives parameters, generates a placeholder image with the data written on it,
    and returns it as a Base64-encoded data URL.
    """
    width, height = 400, 400
    img = Image.new("RGB", (width, height), color="white")
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", 15)
    except IOError:
        font = ImageFont.load_default()

    draw.text((10, 10), "Image Generated with Parameters:", fill="black", font=font)
    draw.text((20, 40), f"- Rule: {params.rule}", fill="black", font=font)
    draw.text((20, 60), f"- Cell Space: {params.cell_space}", fill="black", font=font)
    draw.text((20, 80), f"- Evolutions: {params.num_evolutions}", fill="black", font=font)
    draw.text((20, 100), f"- Init Method: {params.init_method}", fill="black", font=font)
    draw.text((20, 120), f"- Print Method: {params.print_method}", fill="black", font=font)
    draw.rectangle([0, 0, width - 1, height - 1], outline="black", width=2)

    buffered = io.BytesIO()
    img.save(buffered, format="PNG")

    img_str = base64.b64encode(buffered.getvalue()).decode()
    img_data_url = f"data:image/png;base64,{img_str}"

    return {"image_data": img_data_url}


if __name__ == "__main__":
    # To run this file, use: uvicorn src.web-app:app --reload
    uvicorn.run(app, host="127.0.0.1", port=8000)
