// Define la URL base de la IP y el puerto donde se ejecuta el servidor Flask
const BASE_URL = 'http://127.0.0.1:5000';


document.getElementById('runScript').addEventListener('click', () => {
  // Muestra una alerta indicando que el script está empezando
  alert('El script está comenzando a ejecutarse. Esto puede tomar un momento.');

  // Realiza la solicitud para ejecutar el script
  fetch(`${BASE_URL}/run_script`)
    .then(response => response.json())
    .then(data => {
      // Muestra una alerta indicando que el script ha terminado
      alert('El script ha terminado de ejecutarse.');
      document.getElementById('output').innerHTML = data.message;
    })
    .catch(error => {
      // Muestra una alerta en caso de error
      alert('Error: ' + error.message);
      document.getElementById('output').innerHTML = 'Error: ' + error.message;
    });
});

document.getElementById('runNewScript').addEventListener('click', () => {
  // Muestra una alerta indicando que el script está empezando
  alert('El script está comenzando a ejecutarse. Esto puede tomar un momento.');

  // Realiza la solicitud para ejecutar el script
  fetch(`${BASE_URL}/run_newscript`)
    .then(response => response.json())
    .then(data => {
      // Muestra una alerta indicando que el script ha terminado
      alert('El script ha terminado de ejecutarse.');
      document.getElementById('output').innerHTML = data.message;
    })
    .catch(error => {
      // Muestra una alerta en caso de error
      alert('Error: ' + error.message);
      document.getElementById('output').innerHTML = 'Error: ' + error.message;
    });
});



document.getElementById('get-data').addEventListener('click', () => {
  fetch(`${BASE_URL}/get_all_data`)  // Cambia la URL a la ruta correcta de tu API
    .then(response => response.json())
    .then(data => {
      // Limpia el contenido anterior si lo hubiera
      document.getElementById('data-container').innerHTML = '';

      // Crea una tabla y su encabezado
      const table = document.createElement('table');
      const tableHeader = document.createElement('tr');
      tableHeader.innerHTML = `
              <th>CIUDAD</th>
              <th>PROVINCIA</th>
              <th>GRADOS</th>
              <th>FECHA</th>
              <th>HORA</th>
              <th>TIPO</th>
          `;
      table.appendChild(tableHeader);

      // Agrega solo los 2 últimos elementos a la tabla
      const startIndex = Math.max(0, data.length - 2);
      for (let i = startIndex; i < data.length; i++) {
        const item = data[i];
        const tableRow = document.createElement('tr');
        tableRow.innerHTML = `
                  <td>${item.CIUDAD}</td>
                  <td>${item.PROVINCIA}</td>
                  <td>${item.GRADOS}</td>
                  <td>${item.FECHA}</td>
                  <td>${item['HORA MADRID (UTC+2)']}</td>
                  <td>${item.TIPO}</td>
              `;
        table.appendChild(tableRow);
      }

      // Agrega la tabla al contenedor
      document.getElementById('data-container').appendChild(table);
    })
    .catch(error => {
      console.error('Error al obtener datos:', error);
    });

  // Timeout para desparecer la tabla
  setTimeout(() => {
    document.getElementById('data-container').innerHTML = '';
  }
    , 60000); // 60000 milisegundos = 1 minuto

});


document.getElementById('getMap').addEventListener('click', () => {
  // Crea el elemento iframe
  const iframe = document.createElement('iframe');
  iframe.src = `${BASE_URL}/get_map`;
  // iframe.width = '100%'; // Ajusta el ancho del iframe
  iframe.width = '700px'
  iframe.height = '600px'; // Ajusta la altura del iframe

  // Limpia el contenido anterior y agrega el iframe al contenedor
  const mapContainer = document.getElementById('map-container');
  mapContainer.innerHTML = '';
  mapContainer.appendChild(iframe);

  // Establece un temporizador para ocultar el iframe después de 1 minuto
  setTimeout(() => {
    mapContainer.innerHTML = ''; // Quita el iframe
  }, 60000); // 60000 milisegundos = 1 minuto
});
