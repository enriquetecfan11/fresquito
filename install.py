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
        subprocess.check_call(['pip', 'install', package])
        print(f'Paquete {package} instalado correctamente.')
    except subprocess.CalledProcessError:
        print(f'Error al instalar el paquete {package}.')

print('Todos los paquetes necesarios han sido instalados.')
