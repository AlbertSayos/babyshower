// src/script/script.js

// Define la fecha objetivo
const fechaObjetivo = new Date('2024-10-04T00:00:00Z');

// Función para actualizar el contador
function actualizarContador() {
  const ahora = new Date();
  const diferencia = fechaObjetivo - ahora;

  // Calcula días, horas, minutos y segundos restantes
  const dias = Math.floor(diferencia / (1000 * 60 * 60 * 24));
  const horas = Math.floor((diferencia % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  const minutos = Math.floor((diferencia % (1000 * 60 * 60)) / (1000 * 60));
  const segundos = Math.floor((diferencia % (1000 * 60)) / 1000);

  // Actualiza el contenido del contador
  document.getElementById('contador').innerHTML = `Faltan ${dias} días ${horas} horas ${minutos} minutos ${segundos} segundos`;
}

// Actualiza el contador cada segundo
setInterval(actualizarContador, 1000);

// Inicializa el contador al cargar la página
actualizarContador();

const audioPlayer = document.getElementById('audioPlayer');
const botonReproducir = document.getElementById('botonReproducir');

let reproduciendo = false;

botonReproducir.addEventListener('click', () => {
  if (!reproduciendo) {
    audioPlayer.play();
    botonReproducir.textContent = 'Pausa';
    reproduciendo = true;
  } else {
    audioPlayer.pause();
    botonReproducir.textContent = 'Reproducir';
    reproduciendo = false;
  }
});
