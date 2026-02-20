# Fresquito

<div style="display: flex; justify-content: center; align-items: center; gap: 8px; flex-wrap: wrap;">
  <img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License">
  <img src="https://img.shields.io/badge/version-0.1.0-green.svg" alt="Version">
  <img src="https://img.shields.io/badge/build-passing-brightgreen.svg" alt="Build">
  <img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" alt="PRs">
</div>

> Get the coldest and hottest towns in Spain in (near) real time and serve them via a REST API and a static web UI.

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Getting Started](#-getting-started)
- [API Endpoints](#-api-endpoints)
- [Configuration](#-configuration)
- [Docker](#-docker)
- [Roadmap](#-roadmap)
- [Authors](#-authors)

## ✨ Features

- **Real-time extremes** — Fetches weather for towns in Spain (El Tiempo API), computes the coldest and hottest town and exposes them via API and UI.
- **Pipeline** — Loads a town index (CSV with `pelmorex_id`), scrapes weather (threaded), merges data, finds extremes, writes CSVs and generates a Folium map.
- **REST API** — Flask API with CORS: run pipeline, get all weather data as JSON, serve the map and static frontend.
- **Interactive map** — Folium map showing coldest and hottest locations; served as `map.html` and via `GET /get_map`.
- **Configurable** — Data directory, CSV paths, max threads, number of locations and geocoder user agent via environment variables.
- **Layered architecture** — Clean separation: domain → application → infrastructure → interface (Flask only in interface).
- **Docker-ready** — Build and run with Docker; helper scripts in `scripts/` for createcontainer, startcontainer and logs.

## 🛠 Tech Stack

- **Backend:** Python 3.10+, Flask, flask-cors
- **Data & scraping:** pandas, requests, beautifulsoup4, lxml, geopy, folium
- **Deploy:** Docker, nginx
- **Quality:** Ruff (lint & format), mypy (optional)

## 🚀 Getting Started

1. **Install:** `pip install -e .` (or `pip install -r requirements.txt` then `pip install -e .`).
2. **Data:** Place `town_index.csv` and `new_town_index.csv` in the `data/input/` folder (or set paths via env). All generated CSVs and the map are saved under `data/output/`.
3. **Start API:** From the repo root run `fresquito` or `python -m fresquito` (with `PYTHONPATH=src` if not installed).

The API listens on `http://0.0.0.0:5000`.

## 📡 API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Welcome message |
| `GET` | `/run_script` | Run pipeline (town_index.csv, limited locations) |
| `GET` | `/run_newscript` | Run pipeline (new_town_index.csv, all locations) |
| `GET` | `/get_all_data` | JSON of `datos_tiempo.csv` rows |
| `GET` | `/get_map` | Serves `map.html` |
| `GET` | `/<path:filename>` | Static files from `interfaz/` |

## ⚙️ Configuration

Environment variables (see `.env.example`):

- `FRESQUITO_DATA_DIR` — Directory for all CSV/XLSX and generated files (default: `data`)
- `TOWN_INDEX_PATH`, `NEW_TOWN_INDEX_PATH` — Town index CSVs
- `DATOS_TIEMPO_PATH`, `MAP_PATH`, `OUTPUT_CSV_PATH`, `NGINX_INDEX_PATH`, `WEATHER_DATA_PATH` — Output paths under `data/output/`
- `MAX_THREADS` (default: 8), `NUM_LOCATIONS` (default: 2000 for run_script)
- `GEOCODER_USER_AGENT` — Nominatim user agent

## 🐳 Docker

- **Build:** `docker build -t fresquito .` (or use `scripts/createcontainer.sh`)
- **Run:** `docker run -d -p 5000:5000 --name fresquito fresquito`

The Dockerfile installs the package with `pip install -e .` and runs `fresquito`.

## 🗺 Roadmap

- Keep API contract stable (routes, JSON shape, CSV columns and encoding for `get_all_data`).
- Optional: add test suite and CI; extend pipeline or UI as needed.

## 👥 Authors

**Enrique Rodriguez Vela** — *Full-stack Development*

- GitHub: [@enriquetecfan11](https://github.com/enriquetecfan11)

---

<div align="center">
  Made with ❤️ by <a href="https://github.com/enriquetecfan11">Enrique Rodriguez Vela</a>
</div>
