That **"Deconstruct & Extract" Emerald** palette on Zinc really gives it an enterprise, high-trust finish—clean, deliberate, and modern without looking like an off-the-shelf template.

Here is the finalized, high-impact **`README.md`** tailored to **ScrapeSense** (with no version numbers, the updated palette, and portfolio-ready presentation for your instructor, GitHub, and LinkedIn).

---

### Updated `README.md`

Open `README.md` in your root folder and replace its contents:

```markdown
# ScrapeSense // Automated Market Intelligence Engine

An asynchronous, full-stack market intelligence and web extraction platform built with **FastAPI**, **BeautifulSoup4**, **Pandas**, **Three.js**, and **Chart.js**.

Designed around the **"Deconstruct & Extract" Emerald** architecture—combining resilient data pipelines with a high-trust, responsive analytical dashboard.

---

## Core Architecture & Features

- **Automated Pagination & Polite Crawling:**
  - Robust session management traversing up to 50 catalog pages (1,000 products).
  - Configurable exponential backoff retries, request throttling, and detail-page resolution.
- **Asynchronous Execution & State Management:**
  - Background task worker decoupled from the HTTP request-response cycle.
  - Live state polling tracking percentage completion, active page depth, and item counts in real time.
- **High-Trust Analytical HUD:**
  - Integrated 3D ambient particle system rendered via **Three.js**.
  - Dynamic KPI metric surfaces with glare/physics perspective powered by **Vanilla-Tilt**.
  - Reactive **Chart.js** visualizations mapping price tier frequencies and star rating distributions.
  - Real-time catalog filtering by title and star tier without page refreshes.
- **Enterprise Data Normalization:**
  - Automated currency stripping to native floating points.
  - Natural-language ratings mapped to discrete integers (`1`–`5`).
  - Strict deduplication based on canonical product URLs.
  - One-click direct streaming exports to **CSV** and **Excel (.xlsx)** formats.
- **Interactive REST Documentation:**
  - Native OpenAPI/Swagger specification accessible at `/docs`.

---

## Technical Stack

* **Backend & API:** Python 3.11+, FastAPI, Starlette, Uvicorn, Requests, BeautifulSoup4
* **Data Engineering & Pipeline:** Pandas, NumPy, OpenPyXL, Matplotlib
* **Client & UI Architecture:** HTML5, Modern Scaffolding CSS, JavaScript (ES6+)
* **Interactive Graphics & Viz:** Three.js (WebGL), Chart.js, Vanilla-Tilt.js, FontAwesome

---

## Repository Layout

```text
EcommerceProductScraper/
│
├── scraper/
│   ├── crawler.py          # Session pooling, pagination loops & progress hooks
│   ├── parser.py           # BeautifulSoup card extraction & deep product details
│   ├── cleaner.py          # Regex cleaning, dtype casting & deduplication
│   └── analyzer.py         # Summary statistics & Matplotlib graphic exports
│
├── static/
│   ├── css/style.css       # Deconstruct Emerald & Zinc layout styling
│   └── js/app.js           # Three.js 3D canvas, Chart.js engine & polling logic
│
├── templates/
│   └── index.html          # Dynamic control console & data grid
│
├── data/                   # Internal caching layer
├── output/                 # Exported datasets (CSV, Excel) & analytical charts
├── notebooks/              # Jupyter notebook for exploratory data analysis
├── main.py                 # Unified FastAPI application & execution entrypoint
├── requirements.txt        # Production dependencies
└── README.md

```

---

## Getting Started

### 1. Environment Setup

```powershell
# Clone or enter repository directory
cd W:\Projects\EcommerceProductScraper

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install project dependencies
pip install -r requirements.txt

```

### 2. Launch the Application

```powershell
python main.py

```

* **Interactive Dashboard:** `http://127.0.0.1:8000`
* **Swagger API Docs:** `http://127.0.0.1:8000/docs`

---

## API Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/` | Serves the interactive 3D web dashboard |
| `POST` | `/api/scrape?pages={n}&fetch_details={bool}` | Queues an asynchronous scraping background job |
| `GET` | `/api/status` | Real-time polling endpoint for job progress and console logs |
| `GET` | `/api/products?search={q}&rating={n}` | Filtered catalog query |
| `GET` | `/api/analytics` | Statistical aggregates and chart-ready distribution buckets |
| `GET` | `/api/export/{csv|excel}` | Direct downloadable exports of the cleaned dataset |

