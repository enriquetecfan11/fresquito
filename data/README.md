# Datos (CSV / XLSX)

En esta carpeta se guardan todos los archivos de datos del proyecto.

**Entrada (índices de pueblos):**
- `town_index.csv` – Índice de localidades (pelmorex_id, name, province)
- `new_town_index.csv` – Índice alternativo

**Salida (generados por el pipeline):**
- `datos_tiempo.csv` – Registro de pueblos más fríos y más calurosos por ejecución
- `output.csv` – Resultado completo del merge (índice + temperaturas)
- `map.html` – Mapa Folium (frío/calor)
- `index.nginx-debian.html` – Misma mapa para nginx
- `weather_data.csv` – Datos auxiliares de tiempo (si se usan)

Puedes hacer backup o versionar solo los que te interesen (por ejemplo los índices); los generados se pueden ignorar en git con `.gitignore`.
