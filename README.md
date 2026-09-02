# ScrapeSense: Multi-Vendor E-Commerce Intelligence Engine

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Render](https://img.shields.io/badge/Render-Deployed-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://scrapesense-t7or.onrender.com)
[![Status](https://img.shields.io/badge/Service-Active-10B981?style=for-the-badge)](https://scrapesense-t7or.onrender.com)

ScrapeSense is a full-stack, asynchronous multi-vendor market intelligence platform engineered to concurrently extract, clean, normalize, and analyze retail catalog data across **Amazon**, **eBay**, and **Alibaba**.

Built with an asynchronous FastAPI backend and a reactive glassmorphic frontend rendered in the custom **"Deconstruct & Extract" Emerald** design system, ScrapeSense provides real-time market comparison, instant price distribution analytics, and structured dataset exports (CSV/XLSX).

---

## Live Links

- **Production URL:** [https://scrapesense-t7or.onrender.com](https://scrapesense-t7or.onrender.com)
- **Interactive API Documentation:** [https://scrapesense-t7or.onrender.com/docs](https://scrapesense-t7or.onrender.com/docs)
- **GitHub Repository:** [https://github.com/Asad-Farooq4421/ScrapeSense](https://github.com/Asad-Farooq4421/ScrapeSense)

---

## Core System Architecture
```text
ScrapeSense Architecture Pipeline
│
├── Client Viewport (Glassmorphic Interface)
│   ├── Three.js 3D Background & Particle Viewport
│   ├── Reactive Chart.js Price Visualizer
│   └── Interactive Vanilla-Tilt.js Product Cards
│
├── API Gateway & Worker Layer (FastAPI / Uvicorn)
│   ├── Async Polling & Live JSON State Handler
│   └── In-Memory Background Task Dispatcher
│
├── Extraction & Scraping Engine (Multi-Vendor Hub)
│   ├── eBay Extractor (BeautifulSoup4 + Clean URL Resolvers)
│   ├── Amazon Crawler (User-Agent Pools + Heuristic Recovery)
│   └── Alibaba Scraper (Wholesale Normalization Engine)
│
├── Reliability & Resilience Layer
│   └── Heuristic Shield (Dynamic Fallback & Non-404 Endpoint Router)
│
├── Data Pipeline & Analytics
│   ├── Regex Parser & Data Normalizer (Clean Pricing & Ratings)
│   └── Pandas Statistical Modeling (Medians, Spreads, Outliers)
│
└── Export & Persistence Engine
    ├── Streamed CSV Generator
    └── OpenPyXL Styled Excel Exporter
```

## Features

- **Concurrent Multi-Vendor Harvesting:** Concurrently queries multiple vendor catalogs using asynchronous thread pools and customized User-Agent rotations.
- **Heuristic Resilience Shield:** Implements intelligent fallback routing to prevent service downtime and eliminate broken 404 links when commercial cloud datacenter IP ranges encounter anti-scraping walls (e.g., Akamai / Cloudflare).
- **Automated Data Normalization:** Standardizes multi-currency pricing strings into clean floating-point numerics, formats ratings to uniform scales, and eliminates vendor tracking wrappers.
- **Reactive Market Visualizations:** Embedded Chart.js analytical dashboards calculate real-time platform price averages, market spreads, and category distributions.
- **Instant Export Pipelines:** Generates enterprise-ready `multi_vendor_products.csv` and styled `.xlsx` spreadsheets on demand directly from in-memory analytical states.
- **Engineered Aesthetic:** Crafted with the "Deconstruct & Extract" Emerald palette (Zinc 50 background `#F4F4F5`, Zinc 900 text, and Emerald 500 accents `#10B981`) paired with interactive 3D particle systems powered by Three.js.

---

## Tech Stack

| Layer | Technologies |
| :--- | :--- |
| **Backend & ASGI** | Python 3.11+, FastAPI, Uvicorn, Gunicorn, Jinja2 |
| **Extraction & Parsing** | Requests, BeautifulSoup4, Regex URL Sanitizers |
| **Data Processing & Analytics** | Pandas, OpenPyXL, NumPy, Matplotlib |
| **Frontend & Visualization** | Vanilla JavaScript (ES6+), HTML5, CSS3, Chart.js, Three.js, Vanilla-Tilt.js |
| **Cloud Deployment** | Render Cloud Application Platform (Native Linux Web Services) |

---

## Project Structure
ScrapeSense/
├── main.py # FastAPI server, endpoints, and background job state
├── requirements.txt # Production dependencies
├── .gitignore # Ignored environments, logs, and artifacts
├── README.md # System documentation
├── scraper/
│ ├── init.py # Module initialization
│ ├── crawler.py # Multi-platform scraping coordinator & resilience logic
│ ├── parser.py # DOM structure parsers for eBay, Amazon, and Alibaba
│ ├── cleaner.py # Regex-based currency and rating normalization
│ └── analyzer.py # Descriptive statistical modeling & metrics
├── static/
│ ├── css/
│ │ └── style.css # "Deconstruct & Extract" Emerald styling
│ └── js/
│ └── app.js # Client UI state, Three.js engine, and Chart.js integration
└── templates/
└── index.html # Core glassmorphic operational dashboard

text

---

## Local Development Setup

1. **Clone the repository:**

```bash
git clone https://github.com/Asad-Farooq4421/ScrapeSense.git
cd ScrapeSense
Create and activate a virtual environment:

bash
# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
Install dependencies:

bash
pip install -r requirements.txt
Run the local development server:

bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
Access the application at http://127.0.0.1:8000 and view interactive Swagger docs at http://127.0.0.1:8000/docs.

Cloud Deployment (Render)
This repository is pre-configured for automated builds on Render:

Build Command: pip install -r requirements.txt

Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT

Healthcheck Path: / (Supports both GET and HEAD requests)

Future Enhancements & Technical Roadmap
Residential Proxy & Anti-Bot Bypass Integration: Integrate specialized scraping proxy layers (e.g., ScraperAPI, ZenRows, or BrightData) with automated CAPTCHA-solving upstream. This will enable direct residential IP rotation, allowing live cloud extraction on Render without triggering Cloudflare, Akamai, or DataDome perimeter challenges.

Headless Browser Automation: Incorporate Playwright / Camoufox worker pools for executing vendor single-page applications (SPAs) and handling client-side JavaScript hydration.

Persistent Distributed Storage: Transition local file and in-memory session caches to a cloud relational database (PostgreSQL via SQLAlchemy) and Amazon S3 for archival dataset storage.

Asynchronous Message Broker: Offload heavy concurrent multi-vendor crawling tasks onto a Celery/Redis task queue with WebSocket streaming progress feeds.

Automated Price Alerts: Implement user authentication and email notifications when a tracked product crosses a target price threshold.