function irADireccion() {
    const a = document.createElement('a');
    a.href = "https://www.google.com/maps/place/Galvarino+2493,+Chiguayante,+B%C3%ADo+B%C3%ADo,+Chile/@-36.9136494,-73.0294044,17z/data=!3m1!4b1!4m5!3m4!1s0x9669b762e7ddbc1f:0xbc240be36e8b1b9b!8m2!3d-36.9136537!4d-73.0268295?hl=es&entry=ttu";
    a.target = "_blank";
    a.click();
}
// Redirige a la página de regalos
function irARegalos() {
    window.location.href = "/regalos";
}

// Obtener los elementos del DOM
const emergente = document.getElementById('emergente');
const openEmergenteBtn = document.getElementById('openEmergenteBtn');
const closeEmergenteBtn = document.getElementById('closeEmergenteBtn');

// Mostrar la ventana emergente al hacer clic en el botón de abrir
openEmergenteBtn.onclick = function() {
    emergente.style.display = 'block';
}

// Cerrar la ventana emergente al hacer clic en el botón de cerrar
closeEmergenteBtn.onclick = function() {
    emergente.style.display = 'none';
}

// Cerrar la ventana emergente al hacer clic fuera del contenido de la ventana
window.onclick = function(event) {
    if (event.target == emergente) {
        emergente.style.display = 'none';
    }
}

function toggleAsistencia() {
      fetch('/enviar')
          .then(response => response.json())
          .then(data => {
              const whatsappLink = data.whatsapp_link;
              // Crear un elemento <a> dinámicamente
              const a = document.createElement('a');
              a.href = whatsappLink;
              a.target = "_blank"; // Establecer el target
              // Añadir el enlace al DOM y hacer clic
              document.body.appendChild(a);
              a.click();
              // Remover el enlace después de hacer clic
              document.body.removeChild(a);
          })
          .catch(error => console.error('Error al enviar el mensaje:', error));
  }
  
  function toggleAsistencia2() {
    const telefono = "+56931341473"; // Número de teléfono de destino
    const mensaje = "Hola! 🤗 con gusto asistiré al Baby Shower 💝 de Gianna 👶🏻👑"; // Mensaje a enviar
    const whatsappLink = `https://api.whatsapp.com/send?phone=${telefono}&text=${encodeURIComponent(mensaje)}`;

    // Crear un elemento <a> dinámicamente
      const a = document.createElement('a');
    a.href = whatsappLink;
    a.target = "_blank"; // Establecer el target para abrir en una nueva pestaña
    // Añadir el enlace al DOM y hacer clic
    document.body.appendChild(a);
    a.click();
    // Remover el enlace después de hacer clic
    document.body.removeChild(a);
}

function toggleMute() {
var music = document.getElementById('background-music');
var button = document.getElementById('mute-button');

if (music.muted) {
    music.muted = false;
    button.textContent = '🔊';
} else {
    music.muted = true;
    button.textContent = '🔇';
}
}


/*-----------------------------------------------REGALO------------------------------*/



