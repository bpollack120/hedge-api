
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from hedge_model import run_dynamic_hedge_analysis
import os

app = FastAPI()

# ✅ Root endpoint for Render health check or browser test
@app.get("/")
def read_root():
    return {"message": "🚀 Hedge API is live!"}

# ✅ Request schema for hedge analysis
class HedgeRequest(BaseModel):
    ticker: str
    start_date: str  # YYYY-MM-DD
    end_date: str    # YYYY-MM-DD

# ✅ Main POST endpoint to trigger simulation
@app.post("/hedge")
def hedge(request: HedgeRequest):
    try:
        # Run hedge logic
        run_dynamic_hedge_analysis(
            request.ticker.upper(), 
            request.start_date, 
            request.end_date
        )

        # File output paths
        base_path = os.path.join(os.path.dirname(__file__), "excel_exports")
        excel_path = os.path.join(base_path, f"{request.ticker.upper()}_dynamic_hedge_output.xlsx")
        plot_path = os.path.join(base_path, f"{request.ticker.upper()}_dynamic_hedge_plot.png")

        if not os.path.exists(excel_path) or not os.path.exists(plot_path):
            raise FileNotFoundError("Simulation completed but output files not found.")

        return {
            "message": "✅ Hedge simulation completed.",
            "excel_file": f"/excel_exports/{request.ticker.upper()}_dynamic_hedge_output.xlsx",
            "plot_file": f"/excel_exports/{request.ticker.upper()}_dynamic_hedge_plot.png"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
