// Define la URL base de la IP y el puerto donde se ejecuta el servidor Flask
const BASE_URL = 'http://127.0.0.1:5000';


document.getElementById('runScript').addEventListener('click', () => {
  fetch(`${BASE_URL}/run_script`)
      .then(response => response.json())
      .then(data => {
          document.getElementById('output').innerHTML = data.message;
      })
      .catch(error => {
          document.getElementById('output').innerHTML = 'Error: ' + error.message;
      });
});

document.getElementById('get-data').addEventListener('click', () => {
  fetch(`${BASE_URL}/get_all_data`)  // Cambia la URL a la ruta correcta de tu API
      .then(response => response.json())
      .then(data => {
          // Limpia el contenido anterior si lo hubiera
          document.getElementById('data-container').innerHTML = '';

          // Itera sobre los datos y crea elementos HTML para mostrarlos
          data.forEach(item => {
              const dataItem = document.createElement('div');
              dataItem.className = 'data-item';
              dataItem.innerHTML = `
                  <p>CIUDAD: ${item.CIUDAD}</p>
                  <p>PROVINCIA: ${item.PROVINCIA}</p>
                  <p>GRADOS: ${item.GRADOS}</p>
                  <p>FECHA: ${item.FECHA}</p>
                  <p>HORA MADRID (UTC+2): ${item['HORA MADRID (UTC+2)']}</p>
                  <p>HORA UTC: ${item['HORA UTC']}</p>
                  <p>TIPO: ${item.TIPO}</p>
              `;
              document.getElementById('data-container').appendChild(dataItem);
          });
      })
      .catch(error => {
          console.error('Error al obtener datos:', error);
      });
});


document.getElementById('getMap').addEventListener('click', () => {
  // Redirecciona a la página que muestra el mapa
  window.location.href = '${BASE_URL}/get_map';
});

document.getElementById('test').addEventListener('click', () => {
  console.log("Testing");
});