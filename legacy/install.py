import subprocess

# Lista de paquetes que se deben instalar
required_packages = [
    'pandas',
    'requests',
    'beautifulsoup4',
    'geopy',
    'folium',
    'datetime',
    'lxml',
    'flask',
    'flask-cors'
]

# Instalando los paquetes uno por uno
for package in required_packages:
    try:
        subprocess.check_call(['pip2', 'install', package])
        print('Paquete {} instalado correctamente.'.format(package))
    except subprocess.CalledProcessError:
        print('Error al instalar el paquete {}.'.format(package))
