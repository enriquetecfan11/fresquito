# Datos (CSV / XLSX)

En esta carpeta se guardan todos los archivos de datos del proyecto, organizados en **input** (entrada) y **output** (generados por el pipeline).

```
data/
├── README.md
├── input/                    # Entrada: versionar / backup
│   ├── town_index.csv
│   ├── new_town_index.csv
│   └── meteorologia.csv
└── output/                  # Salida: generados (opcional .gitignore)
    ├── datos_tiempo.csv
    ├── output.csv
    ├── weather_data.csv
    ├── map.html
    └── index.nginx-debian.html
```

**Entrada (`input/`):**
- `town_index.csv` – Índice de localidades (pelmorex_id, name, province)
- `new_town_index.csv` – Índice alternativo
- `meteorologia.csv` – Datos auxiliares (legacy)

**Salida (`output/`):**
- `datos_tiempo.csv` – Registro de pueblos más fríos y más calurosos por ejecución
- `output.csv` – Resultado completo del merge (índice + temperaturas)
- `map.html` – Mapa Folium (frío/calor)
- `index.nginx-debian.html` – Mismo mapa para nginx
- `weather_data.csv` – Datos auxiliares de tiempo (si se usan)

Puedes hacer backup o versionar solo `input/`; los archivos en `output/` se pueden ignorar en git con `data/output/` en `.gitignore`.
