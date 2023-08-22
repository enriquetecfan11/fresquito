# Usar una imagen base de Python
FROM python:3.9

# Directorio de trabajo en el contenedor
WORKDIR /app

# Copiamos los scripts para su ejecución
COPY main.py /app/
COPY install.py /app/


# Actualizar pip
#RUN pip install --upgrade pip#

# Ejecutar el script install.py para instalar las dependencias
#RUN python install.py

# Instalar Nginx
#RUN apt-get update && apt-get install -y nginx

# Configurar Nginx para servir archivos estáticos
#COPY nginx-default /etc/nginx/sites-available/default

# CMD para iniciar Nginx y ejecutar el script main.py cada 1 hora
#CMD service nginx start && while true; do python main.py; sleep 1h; done