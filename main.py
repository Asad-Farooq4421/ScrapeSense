import os
import sys
import logging
import uvicorn
import pandas as pd
from fastapi import FastAPI, BackgroundTasks, Query, HTTPException, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from scraper.crawler import MultiVendorCrawler
from scraper.cleaner import clean_dataset

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

CSV_PATH = os.path.join(OUTPUT_DIR, "multi_vendor_products.csv")
EXCEL_PATH = os.path.join(OUTPUT_DIR, "multi_vendor_products.xlsx")

os.makedirs(OUTPUT_DIR, exist_ok=True)

logger = logging.getLogger("ScraperLogger")
logger.setLevel(logging.INFO)
if not logger.handlers:
    fh = logging.FileHandler("scraper.log", encoding="utf-8")
    fh.setFormatter(logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s"))
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
    logger.addHandler(fh)
    logger.addHandler(sh)

app = FastAPI(title="ScrapeSense // Multi-Platform Search Engine")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# Global Job State
search_job = {
    "status": "idle",       # idle | running | completed | failed
    "progress": 0,
    "query": "",
    "total_records": 0,
    "error_message": "",
    "logs": []
}

def log_terminal(msg: str):
    search_job["logs"].append(msg)
    if len(search_job["logs"]) > 40:
        search_job["logs"].pop(0)

def bg_search_task(query: str):
    global search_job
    try:
        search_job["status"] = "running"
        search_job["progress"] = 10
        search_job["query"] = query
        search_job["error_message"] = ""
        search_job["logs"] = []

        def on_progress(pct, msg):
            search_job["progress"] = pct
            log_terminal(msg)

        crawler = MultiVendorCrawler()
        raw_results = crawler.search_all_platforms(query, progress_callback=on_progress)

        if not raw_results:
            raise ValueError(f"No products found across Amazon, eBay, or Alibaba for '{query}'.")

        log_terminal("Preprocessing and normalizing pricing & data structures...")
        df = clean_dataset(raw_results)

        df.to_csv(CSV_PATH, index=False, encoding="utf-8")
        df.to_excel(EXCEL_PATH, index=False, engine="openpyxl")

        search_job["total_records"] = len(df)
        search_job["progress"] = 100
        search_job["status"] = "completed"
        log_terminal(f"Search complete. {len(df)} products aggregated & stored.")

    except Exception as exc:
        search_job["status"] = "failed"
        search_job["error_message"] = str(exc)
        log_terminal(f"[ERROR] {str(exc)}")
        logger.error(f"Search failed: {exc}", exc_info=True)

@app.api_route("/", methods=["GET", "HEAD"])
def dashboard(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.post("/api/search")
def run_search(background_tasks: BackgroundTasks, query: str = Query(..., min_length=2)):
    if search_job["status"] == "running":
        raise HTTPException(status_code=409, detail="A query is already actively executing.")
    background_tasks.add_task(bg_search_task, query)
    return {"message": "Multi-vendor scrape triggered.", "query": query}

@app.get("/api/status")
def get_status():
    return search_job

@app.get("/api/products")
def get_products(source: str = "", min_price: float = None, max_price: float = None):
    if not os.path.exists(CSV_PATH):
        return {"total": 0, "products": []}

    try:
        df = pd.read_csv(CSV_PATH).fillna("")
        if source:
            df = df[df["source"].str.lower() == source.lower()]
        if min_price is not None:
            df = df[df["price"] >= min_price]
        if max_price is not None:
            df = df[df["price"] <= max_price]

        return {"total": len(df), "products": df.to_dict(orient="records")}
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))

@app.get("/api/analytics")
def get_analytics():
    if not os.path.exists(CSV_PATH):
        return {"ready": False}

    try:
        df = pd.read_csv(CSV_PATH)
        if df.empty:
            return {"ready": False}

        # Average price per platform
        platform_means = df.groupby("source")["price"].mean().round(2).to_dict()
        platform_counts = df["source"].value_counts().to_dict()

        return {
            "ready": True,
            "total_products": int(len(df)),
            "avg_price": round(float(df["price"].mean()), 2),
            "min_price": round(float(df["price"].min()), 2),
            "max_price": round(float(df["price"].max()), 2),
            "charts": {
                "platform_comparison": {
                    "labels": list(platform_means.keys()),
                    "averages": list(platform_means.values())
                },
                "platform_share": {
                    "labels": list(platform_counts.keys()),
                    "counts": list(platform_counts.values())
                }
            }
        }
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))

@app.get("/api/export/{file_type}")
def export_file(file_type: str):
    if file_type == "csv":
        if not os.path.exists(CSV_PATH):
            raise HTTPException(status_code=404, detail="Dataset not found. Search first.")
        return FileResponse(CSV_PATH, media_type="text/csv", filename="multi_vendor_products.csv")
    elif file_type == "excel":
        if not os.path.exists(EXCEL_PATH):
            raise HTTPException(status_code=404, detail="Dataset not found. Search first.")
        return FileResponse(EXCEL_PATH, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", filename="multi_vendor_products.xlsx")
    raise HTTPException(status_code=400, detail="Invalid export type.")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)