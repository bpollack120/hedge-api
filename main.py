
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from hedge_model import run_dynamic_hedge_analysis
import os

app = FastAPI()

class HedgeRequest(BaseModel):
    ticker: str
    start_date: str
    end_date: str

@app.post("/hedge")
def hedge(request: HedgeRequest):
    try:
        run_dynamic_hedge_analysis(request.ticker.upper(), request.start_date, request.end_date)
        excel_path = f"excel_exports/{request.ticker.upper()}_dynamic_hedge_output.xlsx"
        plot_path = f"excel_exports/{request.ticker.upper()}_dynamic_hedge_plot.png"
        return {
            "message": "Hedge simulation completed.",
            "excel_url": excel_path,
            "plot_url": plot_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
