from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

app = FastAPI(title="Prediction API")

# Mount templates and static files
templates = Jinja2Templates(directory="templates")

# Simple prediction function (replace with your actual model)
def predict_value(input_data: float) -> float:
    """Simple prediction function - replace with your actual model"""
    return input_data * 2.5 + 3.2  # Example prediction

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})

@app.get("/predict/{input_value}")
async def get_prediction(input_value: float):
    """API endpoint for prediction"""
    prediction = predict_value(input_value)
    return {
        "input_value": input_value,
        "prediction": round(prediction, 4),
        "message": "Prediction successful"
    }

@app.get("/streamlit")
async def streamlit_redirect():
    """Redirect to Streamlit app (run streamlit separately)"""
    return {"message": "Run Streamlit with: streamlit run templates/streamlit_app.py"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)