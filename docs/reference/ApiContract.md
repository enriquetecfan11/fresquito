# Contrato de la API

Este documento describe las rutas, formatos de respuesta y CSV que **no deben cambiar** para no romper clientes ni la UI.

## Rutas y métodos

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/` | Mensaje de bienvenida. |
| `GET` | `/run_script` | Ejecuta el pipeline con `town_index.csv` (límite de localidades). |
| `GET` | `/run_newscript` | Ejecuta el pipeline con `new_town_index.csv` (todas las localidades). |
| `GET` | `/get_all_data` | Devuelve en JSON el contenido de `datos_tiempo.csv`. |
| `GET` | `/get_map` | Sirve el fichero `map.html`. |
| `GET` | `/<path:filename>` | Sirve estáticos desde `interfaz/`. |

## Formato de respuestas JSON

- **`GET /run_script` y `GET /run_newscript`**
  - Éxito: `{"message": "Script ejecutado correctamente."}`
  - Error: `{"error": "..."}`

- **`GET /get_all_data`**
  - Lista de objetos, uno por fila del CSV `datos_tiempo.csv`.
  - Cada objeto tiene las mismas claves que las columnas del CSV (ver abajo).

## Formato CSV `datos_tiempo.csv`

Encoding de lectura en la API: **iso-8859-1**.

Columnas:

- **TIPO** — Frío o calor.
- **CIUDAD**
- **PROVINCIA**
- **GRADOS**
- **FECHA**
- **HORA UTC**
- **HORA MADRID (UTC+2)**

Cualquier cambio en estas columnas o en el encoding debe mantenerse compatible con lo que consume `get_all_data`.
