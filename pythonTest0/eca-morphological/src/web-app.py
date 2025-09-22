import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from PIL import ImageDraw, ImageFont
import io
import base64
import ca_class


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
    eca_rule_number = int(params.rule)

    eca_size = int(params.cell_space)
    eca_evolutions = int(params.num_evolutions)
    eca_init_method = params.init_method
    eca_print_method = params.print_method  

    eca = ca_class.Eca(rule_number=eca_rule_number)
    eca.define_evolution_config(
        size=eca_size, evolutions=eca_evolutions, print_method=eca_print_method, init_method=eca_init_method
    )
    eca.evolution()
    print(eca)
    _width, _height = 400, 400
    #img = Image.new("RGB", (width, height), color="white")
    img = eca.print_history()
    #print(img)
    ImageDraw.Draw(img)

    try:
        ImageFont.truetype("arial.ttf", 15)
    except IOError:
        ImageFont.load_default()

    buffered = io.BytesIO()
    img.save(buffered, format="PNG")

    img_str = base64.b64encode(buffered.getvalue()).decode()
    img_data_url = f"data:image/png;base64,{img_str}"

    return {"image_data": img_data_url}


if __name__ == "__main__":
    # To run this file, use: uvicorn src.web-app:app --reload
    uvicorn.run(app, host="127.0.0.1", port=8000)
