# Usar una imagen base de Python
FROM python:3.9

# Directorio de trabajo en el contenedor
WORKDIR /app

# Copiar los scripts necesarios al contenedor
COPY main.py /app/main.py
COPY install.py /app/install.py

# Copiar los archivos necesarios al contenedor
COPY output.csv /app/
COPY town_index.csv /app/
COPY index.nginx-debian.html /app/

# Actualizar pip
RUN sudo pip install --upgrade pip

# Ejecutar el script install.py para instalar las dependencias
RUN python install.py

# Instalar Nginx
RUN apt-get update && apt-get install -y nginx

# Configurar Nginx para servir archivos estáticos
COPY nginx-default /etc/nginx/sites-available/default

# CMD para iniciar Nginx y ejecutar el script main.py cada 1 hora
CMD service nginx start && while true; do python main.py; sleep 1h; done