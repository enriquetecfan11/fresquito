# AGENTS.md – Fresquito

Guía para agentes de IA y desarrolladores: cómo está organizado el proyecto, dónde tocar cada cosa y qué mantener intacto.

---

## Qué hace el proyecto

- **Objetivo:** Obtener en tiempo (casi) real el pueblo más frío y el más caluroso de España y servirlos vía API y una UI estática.
- **Flujo:** Lee un índice de localidades (CSV con `pelmorex_id`), consulta la API de El Tiempo, hace merge, calcula extremos, guarda resultados en CSV y genera un mapa Folium (frío/calor). Todo se expone por una API Flask.
- **Stack:** Python 3.10+, Flask, flask-cors, pandas, requests, geopy, folium. Despliegue con Docker.

---

## Arquitectura (capas)

El código está en `src/fresquito/` con cuatro capas. Las dependencias van hacia dentro: **interface → application → infrastructure → domain**.

| Capa | Ruta | Responsabilidad |
|------|------|-----------------|
| **domain** | `src/fresquito/domain/` | Modelos de negocio (dataclasses). Sin Flask ni I/O. |
| **application** | `src/fresquito/application/` | Config, orquestación del pipeline, servicios que exponen “run pipeline”, “get data”, “get map path”. |
| **infrastructure** | `src/fresquito/infrastructure/` | Scraping (El Tiempo API), geocoding (Nominatim), almacenamiento (CSV, Folium). |
| **interface** | `src/fresquito/interface/` | Solo HTTP: app Flask, CORS, rutas que delegan en application. |

**Regla:** La interface no importa infrastructure ni domain directamente para lógica; usa solo application (config + services). El pipeline (application) usa infrastructure y domain.

---

## Dónde está cada cosa

- **Modelos de datos:** `src/fresquito/domain/models.py` (`WeatherRecord`, `ExtremeTown`).
- **Configuración (paths, env):** `src/fresquito/application/config.py`. Por defecto todo CSV/mapa vive en `data/` (`FRESQUITO_DATA_DIR=data`).
- **Orquestación del pipeline:** `src/fresquito/application/run_pipeline.py` → `run_pipeline(...)`.
- **Servicios expuestos a la API:** `src/fresquito/application/services.py` → `run_pipeline_town_index()`, `run_pipeline_new_town_index()`, `get_weather_records()`, `get_map_path()`.
- **Rutas HTTP:** `src/fresquito/interface/api/routes.py` → `register_routes(app)`. Punto de entrada de la app: `src/fresquito/interface/flask_app.py` → `app`, `main()`.
- **Scraping:** `src/fresquito/infrastructure/scraping.py`. **Geocoding:** `src/fresquito/infrastructure/geocoding.py`. **CSV y mapa:** `src/fresquito/infrastructure/storage.py`.
- **Datos (CSV/XLSX):** Carpeta `data/`. Inputs: `town_index.csv`, `new_town_index.csv`. Salidas: `datos_tiempo.csv`, `output.csv`, `map.html`, `index.nginx-debian.html`, etc. Ver `data/README.md`.
- **Front estático:** `interfaz/` (HTML, JS, CSS). Se sirve con la ruta catch-all `/<path:filename>` desde `interfaz/`.
- **Scripts de despliegue:** `scripts/` (createcontainer, startcontainer, logs). **Código viejo:** `legacy/` (no usar).

---

## Contrato que no debe cambiar

- **Rutas y métodos:** `GET /`, `GET /run_script`, `GET /run_newscript`, `GET /get_all_data`, `GET /get_map`, `GET /<path:filename>` (estáticos desde `interfaz/`).
- **Respuestas:** JSON con la misma forma (p. ej. `get_all_data` = lista de objetos por fila del CSV; `run_script`/`run_newscript` = `{"message": "Script ejecutado correctamente."}` o `{"error": "..."}`).
- **Formato CSV:** Columnas de `datos_tiempo.csv` (TIPO, CIUDAD, PROVINCIA, GRADOS, FECHA, HORA UTC, HORA MADRID (UTC+2)) y encoding esperado (iso-8859-1 para lectura en API).

Al añadir o refactorizar, mantener estas rutas y formatos para no romper clientes o la UI.

---

## Cómo ejecutar y comprobar

- **Instalar:** `pip install -r requirements.txt` y opcionalmente `pip install -e .` (desde la raíz del repo).
- **Datos:** Tener `data/town_index.csv` y `data/new_town_index.csv` (o paths vía env). El resto se genera en `data/`.
- **Arrancar API:** Desde la raíz, `fresquito` o `PYTHONPATH=src python -m fresquito`. Escucha en `http://0.0.0.0:5000`.
- **Docker:** `docker build -t fresquito .` y `docker run -d -p 5000:5000 --name fresquito fresquito`. El Dockerfile copia `data/` e instala el paquete; el CMD es `fresquito`.

Comprobar: `GET /` devuelve el mensaje de bienvenida; `GET /get_all_data` devuelve el contenido de `datos_tiempo.csv` en JSON (puede estar vacío si no se ha ejecutado el pipeline).

---

## Convenciones de código

- **Estilo:** PEP 8. Ruff para lint y formato: `ruff check src/`, `ruff format src/`. Config en `pyproject.toml` (line-length 100, target Python 3.10).
- **Tipado:** Anotaciones en funciones públicas; mypy opcional (`mypy src/`), config en `pyproject.toml`.
- **Nombres:** `snake_case` para módulos, funciones y variables; `PascalCase` para clases; `UPPER_SNAKE_CASE` para constantes.
- **Logging:** Usar `logging` (no `print`) para progreso y errores; el módulo raíz está configurado en `flask_app.py`.
- **Tests:** El proyecto no incluye tests; no asumir existencia de `tests/` ni de pytest.

---

## Tareas frecuentes (dónde tocar)

- **Añadir o cambiar una variable de configuración:** `application/config.py` y, si aplica, `.env.example` y README.
- **Cambiar el pipeline (pasos, orden, nuevos outputs):** `application/run_pipeline.py`. Leer/escribir CSV o mapa → `infrastructure/storage.py`; nueva llamada externa → `infrastructure/` (scraping o geocoding).
- **Añadir o modificar un endpoint:** `interface/api/routes.py`. Lógica de negocio en `application/services.py`; la ruta solo delega y devuelve JSON/file.
- **Cambiar formato de un CSV o del mapa:** `infrastructure/storage.py` (cabeceras, escritura, Folium). Mantener contrato de la API (columnas y encoding de `get_all_data`).
- **Añadir una dependencia:** `pyproject.toml` y `requirements.txt`; en Docker solo hace falta que el build instale desde ahí.

---

## Resumen rápido

- **Paquete:** `src/fresquito/` (domain → application → infrastructure → interface).
- **Datos:** Todo en `data/` (inputs y outputs); config vía `application/config.py` y env.
- **Entrada de la app:** `fresquito` (script) o `python -m fresquito`; Flask en `interface/flask_app.py`, rutas en `interface/api/routes.py`.
- **No cambiar:** Rutas actuales, forma del JSON y columnas/encoding del CSV de datos tiempo.
- **Calidad:** ruff + formato; mypy opcional; sin tests.

Para más detalle de arquitectura y flujo, ver `docs/architecture/Architecture.md` y `docs/index.md`.
