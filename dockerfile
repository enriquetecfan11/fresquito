# Usar una imagen base ubuntu python
FROM ubuntu:20.04

# Instalar python
RUN apt-get update
RUN apt-get install -y python3-pip

# Directorio de Trabajo
WORKDIR /app

# Copiamos los scripts para su ejecución
COPY main.py /app/
COPY app.py /app/

# Copiamos los archivos necesarios
COPY output.csv /app/
COPY town_index.csv /app/
COPY weather_data.csv /app/
COPY map.html /app/

# Copiamos la carpeta de interfaz
COPY interfaz /app/interfaz

# Instalamos los paquetes necesarios 'pandas', 'requests', 'beautifulsoup4', 'geopy', 'folium', 'datetime', 'lxml', 'flask',flask-cors'
RUN pip3 install pandas requests beautifulsoup4 geopy folium datetime lxml flask flask-cors

# Permisos para main.py
RUN chmod +x /app/main.py

# Permisos a App.py
RUN chmod +x /app/app.py

# Exponemos el puerto 5000
EXPOSE 5000

# Ejecutamos el script main.py
CMD ["python3", "/app/app.py"]