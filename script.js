// =============================================
// script.js - Semana 5: Proyecto Integrador

// Variable global para contar los registros
let totalRegistros = 0;

// Esperamos a que el DOM esté completamente cargado
document.addEventListener('DOMContentLoaded', function () {

    // Seleccionamos el formulario
    const formulario = document.getElementById('formCurso');

    // Seleccionamos el contenedor donde se mostrarán los registros
    const listaRegistros = document.getElementById('listaRegistros');

    // Seleccionamos el contador de registros
    const contadorRegistros = document.getElementById('contadorRegistros');

    // Seleccionamos los campos del formulario
    const inputNombre = document.getElementById('nombreCurso');
    const inputDescripcion = document.getElementById('descripcionCurso');
    const selectCategoria = document.getElementById('categoriaCurso');

    // Seleccionamos los mensajes de validación
    const errorNombre = document.getElementById('errorNombre');
    const errorDescripcion = document.getElementById('errorDescripcion');
    const errorCategoria = document.getElementById('errorCategoria');

    // =============================================
    // EVENTO SUBMIT del formulario
    // =============================================
    formulario.addEventListener('submit', function (e) {

        // Evitamos que la página se recargue
        e.preventDefault();

        // Obtenemos los valores del formulario
        const nombre = inputNombre.value.trim();
        const descripcion = inputDescripcion.value.trim();
        const categoria = selectCategoria.value;

        // Reseteamos mensajes de error anteriores
        resetarErrores();

        // Validamos que los campos no estén vacíos
        let hayErrores = false;

        if (nombre === '') {
            errorNombre.textContent = '⚠️ El nombre del curso es obligatorio.';
            errorNombre.style.display = 'block';
            inputNombre.classList.add('is-invalid');
            hayErrores = true;
        }

        if (descripcion === '') {
            errorDescripcion.textContent = '⚠️ La descripción es obligatoria.';
            errorDescripcion.style.display = 'block';
            inputDescripcion.classList.add('is-invalid');
            hayErrores = true;
        }

        if (categoria === '') {
            errorCategoria.textContent = '⚠️ Debes seleccionar una categoría.';
            errorCategoria.style.display = 'block';
            selectCategoria.classList.add('is-invalid');
            hayErrores = true;
        }

        // Si hay errores, no continuamos
        if (hayErrores) return;

        // Si todo está bien, creamos el registro
        crearRegistro(nombre, descripcion, categoria);

        // Limpiamos el formulario
        formulario.reset();
        resetarErrores();

        // Mostramos mensaje de éxito
        mostrarMensajeExito();
    });

    // =============================================
    // FUNCIÓN: Crear un nuevo registro en el DOM
    // =============================================
    function crearRegistro(nombre, descripcion, categoria) {

        // Incrementamos el contador
        totalRegistros++;

        // Actualizamos el contador en pantalla
        actualizarContador();

        // Creamos el contenedor principal del registro (div)
        const divRegistro = document.createElement('div');
        divRegistro.classList.add('col-md-6', 'col-lg-4', 'registro-item');
        divRegistro.setAttribute('data-id', totalRegistros);

        // Creamos la card del registro
        const card = document.createElement('div');
        card.classList.add('card', 'h-100', 'p-3', 'border-start', 'border-primary', 'border-3');

        // Creamos el cuerpo de la card
        const cardBody = document.createElement('div');
        cardBody.classList.add('card-body', 'p-0');

        // Creamos el badge de categoría
        const badge = document.createElement('span');
        badge.classList.add('badge', 'bg-primary', 'mb-2');
        badge.textContent = categoria;

        // Creamos el título (nombre del curso)
        const titulo = document.createElement('h5');
        titulo.classList.add('card-title', 'fw-bold');
        titulo.textContent = nombre;

        // Creamos la descripción
        const parrafo = document.createElement('p');
        parrafo.classList.add('card-text', 'text-muted', 'small');
        parrafo.textContent = descripcion;

        // Creamos el botón de eliminar
        const btnEliminar = document.createElement('button');
        btnEliminar.classList.add('btn', 'btn-danger', 'btn-sm', 'mt-2');
        btnEliminar.textContent = '🗑️ Eliminar';

        // Evento click para eliminar el registro
        btnEliminar.addEventListener('click', function () {
            eliminarRegistro(divRegistro);
        });

        // Ensamblamos la card con appendChild
        cardBody.appendChild(badge);
        cardBody.appendChild(titulo);
        cardBody.appendChild(parrafo);
        cardBody.appendChild(btnEliminar);
        card.appendChild(cardBody);
        divRegistro.appendChild(card);

        // Agregamos el registro a la lista
        listaRegistros.appendChild(divRegistro);

        // Mostramos la sección de registros si estaba oculta
        document.getElementById('seccionRegistros').style.display = 'block';
    }

    // =============================================
    // FUNCIÓN: Eliminar un registro del DOM
    // =============================================
    function eliminarRegistro(elemento) {
        elemento.remove();
        totalRegistros--;
        actualizarContador();

        // Si no quedan registros, ocultamos la sección
        if (totalRegistros === 0) {
            document.getElementById('seccionRegistros').style.display = 'none';
        }
    }

    // =============================================
    // FUNCIÓN: Actualizar el contador en pantalla
    // =============================================
    function actualizarContador() {
        contadorRegistros.textContent = totalRegistros;
    }

    // =============================================
    // FUNCIÓN: Resetear mensajes de error
    // =============================================
    function resetarErrores() {
        errorNombre.style.display = 'none';
        errorNombre.textContent = '';
        inputNombre.classList.remove('is-invalid');

        errorDescripcion.style.display = 'none';
        errorDescripcion.textContent = '';
        inputDescripcion.classList.remove('is-invalid');

        errorCategoria.style.display = 'none';
        errorCategoria.textContent = '';
        selectCategoria.classList.remove('is-invalid');
    }

    // =============================================
    // FUNCIÓN: Mostrar mensaje de éxito
    // =============================================
    function mostrarMensajeExito() {
        const alerta = document.getElementById('alertaExito');
        alerta.style.display = 'block';

        // Ocultamos la alerta después de 3 segundos
        setTimeout(function () {
            alerta.style.display = 'none';
        }, 3000);
    }

});