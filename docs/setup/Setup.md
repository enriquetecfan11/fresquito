# Setup y configuración

## Requisitos

- Python 3.10+
- Pip (o entorno virtual recomendado)

## Instalación

Desde la raíz del repositorio:

```bash
pip install -r requirements.txt
pip install -e .
```

Alternativa sin instalar el paquete en modo editable:

```bash
pip install -r requirements.txt
# Arrancar con: PYTHONPATH=src python -m fresquito
```

## Datos

- Colocar en `data/` los CSV de índice: `town_index.csv` y `new_town_index.csv` (o configurar paths por env).
- El resto de archivos (datos_tiempo.csv, output.csv, map.html, etc.) se generan en `data/`. Ver [data/README.md](../../data/README.md).

## Variables de entorno

Copiar `.env.example` a `.env` y ajustar si hace falta.

| Variable | Descripción | Por defecto |
|----------|-------------|-------------|
| `FRESQUITO_DATA_DIR` | Directorio base de CSV y ficheros generados | `data` |
| `TOWN_INDEX_PATH` | Ruta del índice de localidades (script clásico) | `data/town_index.csv` |
| `NEW_TOWN_INDEX_PATH` | Ruta del índice alternativo | `data/new_town_index.csv` |
| `DATOS_TIEMPO_PATH` | CSV de extremos (frío/calor) | `data/datos_tiempo.csv` |
| `MAP_PATH` | Mapa Folium generado | `data/map.html` |
| `OUTPUT_CSV_PATH` | CSV merge completo | `data/output.csv` |
| `NGINX_INDEX_PATH` | Mapa para nginx | `data/index.nginx-debian.html` |
| `WEATHER_DATA_PATH` | CSV auxiliar de tiempo | `data/weather_data.csv` |
| `MAX_THREADS` | Hilos para scraping | `8` |
| `NUM_LOCATIONS` | Límite de localidades en `run_script` | `2000` |
| `GEOCODER_USER_AGENT` | User-Agent para Nominatim | `fresquito-geocoder` |

## Arrancar la API

```bash
fresquito
```

O sin instalar el paquete:

```bash
PYTHONPATH=src python -m fresquito
```

La API escucha en `http://0.0.0.0:5000`.

## Docker

- **Build:** `docker build -t fresquito .` (o `scripts/createcontainer.sh` si existe).
- **Run:** `docker run -d -p 5000:5000 --name fresquito fresquito`.
- **Logs:** `scripts/logs.sh` o `docker logs fresquito`.

El Dockerfile instala con `pip install -e .` y ejecuta `fresquito`.
