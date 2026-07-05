// =============================================
// script.js - Semana 6: Validaciones dinámicas
// y manejo de formularios (Proyecto Integrador)
// =============================================

// Variable global para contar los registros
let totalRegistros = 0;

// Esperamos a que el DOM esté completamente cargado
document.addEventListener('DOMContentLoaded', function () {

    // =============================================
    // REFERENCIAS AL DOM
    // =============================================
    const formulario = document.getElementById('formCurso');
    const listaRegistros = document.getElementById('listaRegistros');
    const contadorRegistros = document.getElementById('contadorRegistros');

    const inputNombre = document.getElementById('nombreCurso');
    const inputDescripcion = document.getElementById('descripcionCurso');
    const selectCategoria = document.getElementById('categoriaCurso');

    const errorNombre = document.getElementById('errorNombre');
    const errorDescripcion = document.getElementById('errorDescripcion');
    const errorCategoria = document.getElementById('errorCategoria');

    const alertaExito = document.getElementById('alertaExito');
    const alertaError = document.getElementById('alertaError');

    // Reglas de validación (fáciles de ajustar si el docente pide otros valores)
    const LONGITUD_MIN_NOMBRE = 5;
    const LONGITUD_MIN_DESCRIPCION = 15;

    // =============================================
    // FUNCIONES AUXILIARES: aplicar estilos de validación
    // =============================================

    // Marca un campo como inválido y muestra su mensaje de error
    function marcarInvalido(campo, elementoError, mensaje) {
        campo.classList.remove('is-valid');
        campo.classList.add('is-invalid');
        elementoError.textContent = mensaje;
        elementoError.style.display = 'block';
    }

    // Marca un campo como válido y oculta su mensaje de error
    function marcarValido(campo, elementoError) {
        campo.classList.remove('is-invalid');
        campo.classList.add('is-valid');
        elementoError.textContent = '';
        elementoError.style.display = 'none';
    }

    // =============================================
    // FUNCIONES DE VALIDACIÓN POR CAMPO (reutilizables)
    // Cada una devuelve true/false y actualiza la UI
    // =============================================

    function validarNombre() {
        const valor = inputNombre.value.trim();

        if (valor === '') {
            marcarInvalido(inputNombre, errorNombre, '⚠️ El nombre del curso es obligatorio.');
            return false;
        }
        if (valor.length < LONGITUD_MIN_NOMBRE) {
            marcarInvalido(inputNombre, errorNombre, `⚠️ Debe tener al menos ${LONGITUD_MIN_NOMBRE} caracteres.`);
            return false;
        }

        marcarValido(inputNombre, errorNombre);
        return true;
    }

    function validarDescripcion() {
        const valor = inputDescripcion.value.trim();

        if (valor === '') {
            marcarInvalido(inputDescripcion, errorDescripcion, '⚠️ La descripción es obligatoria.');
            return false;
        }
        if (valor.length < LONGITUD_MIN_DESCRIPCION) {
            marcarInvalido(inputDescripcion, errorDescripcion, `⚠️ Agrega más detalle (mínimo ${LONGITUD_MIN_DESCRIPCION} caracteres).`);
            return false;
        }

        marcarValido(inputDescripcion, errorDescripcion);
        return true;
    }

    function validarCategoria() {
        if (selectCategoria.value === '') {
            marcarInvalido(selectCategoria, errorCategoria, '⚠️ Debes seleccionar una categoría.');
            return false;
        }

        marcarValido(selectCategoria, errorCategoria);
        return true;
    }

    // Ejecuta las tres validaciones y devuelve true solo si todas pasan
    function validarFormularioCompleto() {
        const nombreValido = validarNombre();
        const descripcionValida = validarDescripcion();
        const categoriaValida = validarCategoria();
        return nombreValido && descripcionValida && categoriaValida;
    }

    // Limpia clases y mensajes de validación (se usa tras un registro exitoso)
    function limpiarEstadosVisuales() {
        [inputNombre, inputDescripcion, selectCategoria].forEach(function (campo) {
            campo.classList.remove('is-valid', 'is-invalid');
        });
        [errorNombre, errorDescripcion, errorCategoria].forEach(function (elemento) {
            elemento.style.display = 'none';
            elemento.textContent = '';
        });
    }

    // =============================================
    // VALIDACIÓN EN TIEMPO REAL (input y blur)
    // =============================================

    inputNombre.addEventListener('input', validarNombre);
    inputNombre.addEventListener('blur', validarNombre);

    inputDescripcion.addEventListener('input', validarDescripcion);
    inputDescripcion.addEventListener('blur', validarDescripcion);

    selectCategoria.addEventListener('input', validarCategoria);
    selectCategoria.addEventListener('blur', validarCategoria);

    // =============================================
    // EVENTO SUBMIT del formulario
    // =============================================
    formulario.addEventListener('submit', function (e) {
        // Evitamos que la página se recargue
        e.preventDefault();

        // Validamos todos los campos antes de registrar
        if (!validarFormularioCompleto()) {
            mostrarMensajeError();
            return;
        }

        // Si todo está bien, obtenemos los valores y creamos el registro
        const nombre = inputNombre.value.trim();
        const descripcion = inputDescripcion.value.trim();
        const categoria = selectCategoria.value;

        crearRegistro(nombre, descripcion, categoria);

        // Limpiamos el formulario y sus estados visuales
        formulario.reset();
        limpiarEstadosVisuales();

        // Mostramos mensaje de éxito
        mostrarMensajeExito();
    });

    // =============================================
    // FUNCIÓN: Crear un nuevo registro en el DOM
    // =============================================
    function crearRegistro(nombre, descripcion, categoria) {
        // Incrementamos el contador
        totalRegistros++;
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

        // Ensamblamos la card
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
    // FUNCIÓN: Mostrar mensaje de éxito
    // =============================================
    function mostrarMensajeExito() {
        alertaError.style.display = 'none';
        alertaExito.style.display = 'block';

        setTimeout(function () {
            alertaExito.style.display = 'none';
        }, 3000);
    }

    // =============================================
    // FUNCIÓN: Mostrar mensaje de error general
    // =============================================
    function mostrarMensajeError() {
        alertaExito.style.display = 'none';
        alertaError.style.display = 'block';

        setTimeout(function () {
            alertaError.style.display = 'none';
        }, 3000);
    }

});