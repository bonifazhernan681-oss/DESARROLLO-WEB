// Arreglo con los cursos registrados (representa los datos del proyecto)
let cursos = [];

document.addEventListener('DOMContentLoaded', function () {

    const formulario = document.getElementById('formCurso');
    const listaRegistros = document.getElementById('listaRegistros');
    const contadorRegistros = document.getElementById('contadorRegistros');
    const seccionRegistros = document.getElementById('seccionRegistros');

    const inputNombre = document.getElementById('nombreCurso');
    const inputDescripcion = document.getElementById('descripcionCurso');
    const selectCategoria = document.getElementById('categoriaCurso');

    const errorNombre = document.getElementById('errorNombre');
    const errorDescripcion = document.getElementById('errorDescripcion');
    const errorCategoria = document.getElementById('errorCategoria');

    const alertaExito = document.getElementById('alertaExito');
    const alertaError = document.getElementById('alertaError');

    const LONGITUD_MIN_NOMBRE = 5;
    const LONGITUD_MIN_DESCRIPCION = 15;

    function marcarInvalido(campo, elementoError, mensaje) {
        campo.classList.remove('is-valid');
        campo.classList.add('is-invalid');
        elementoError.textContent = mensaje;
        elementoError.style.display = 'block';
    }

    function marcarValido(campo, elementoError) {
        campo.classList.remove('is-invalid');
        campo.classList.add('is-valid');
        elementoError.textContent = '';
        elementoError.style.display = 'none';
    }

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

    function validarFormularioCompleto() {
        const nombreValido = validarNombre();
        const descripcionValida = validarDescripcion();
        const categoriaValida = validarCategoria();
        return nombreValido && descripcionValida && categoriaValida;
    }

    function limpiarEstadosVisuales() {
        [inputNombre, inputDescripcion, selectCategoria].forEach(function (campo) {
            campo.classList.remove('is-valid', 'is-invalid');
        });
        [errorNombre, errorDescripcion, errorCategoria].forEach(function (elemento) {
            elemento.style.display = 'none';
            elemento.textContent = '';
        });
    }

    inputNombre.addEventListener('input', validarNombre);
    inputNombre.addEventListener('blur', validarNombre);
    inputDescripcion.addEventListener('input', validarDescripcion);
    inputDescripcion.addEventListener('blur', validarDescripcion);
    selectCategoria.addEventListener('input', validarCategoria);
    selectCategoria.addEventListener('blur', validarCategoria);

    formulario.addEventListener('submit', function (e) {
        e.preventDefault();

        if (!validarFormularioCompleto()) {
            mostrarMensajeError();
            return;
        }

        const nuevoCurso = {
            id: Date.now(),
            nombre: inputNombre.value.trim(),
            descripcion: inputDescripcion.value.trim(),
            categoria: selectCategoria.value
        };
        cursos.push(nuevoCurso);

        renderRegistros();

        formulario.reset();
        limpiarEstadosVisuales();
        mostrarMensajeExito();
    });

    // Recorre el arreglo de cursos y arma las tarjetas en pantalla
    function renderRegistros() {
        listaRegistros.innerHTML = '';

        if (cursos.length === 0) {
            seccionRegistros.style.display = 'none';
            return;
        }
        seccionRegistros.style.display = 'block';

        cursos.forEach(function (curso) {
            const divRegistro = document.createElement('div');
            divRegistro.classList.add('col-md-6', 'col-lg-4', 'registro-item');
            divRegistro.setAttribute('data-id', curso.id);

            const card = document.createElement('div');
            card.classList.add('card', 'h-100', 'p-3', 'border-start', 'border-primary', 'border-3');

            const cardBody = document.createElement('div');
            cardBody.classList.add('card-body', 'p-0');

            const badge = document.createElement('span');
            badge.classList.add('badge', 'mb-2');
            badge.classList.add(curso.categoria === 'Backend' ? 'bg-dark' : 'bg-primary');
            badge.textContent = curso.categoria;

            const titulo = document.createElement('h5');
            titulo.classList.add('card-title', 'fw-bold');
            titulo.textContent = curso.nombre;

            const parrafo = document.createElement('p');
            parrafo.classList.add('card-text', 'text-muted', 'small');
            parrafo.textContent = curso.descripcion;

            const btnEliminar = document.createElement('button');
            btnEliminar.classList.add('btn', 'btn-danger', 'btn-sm', 'mt-2');
            btnEliminar.textContent = '🗑️ Eliminar';
            btnEliminar.addEventListener('click', function () {
                eliminarRegistro(curso.id);
            });

            cardBody.appendChild(badge);
            cardBody.appendChild(titulo);
            cardBody.appendChild(parrafo);
            cardBody.appendChild(btnEliminar);
            card.appendChild(cardBody);
            divRegistro.appendChild(card);

            listaRegistros.appendChild(divRegistro);
        });

        actualizarContador();
    }

    function eliminarRegistro(id) {
        cursos = cursos.filter(function (curso) {
            return curso.id !== id;
        });
        renderRegistros();
    }

    function actualizarContador() {
        contadorRegistros.textContent = cursos.length;
    }

    function mostrarMensajeExito() {
        alertaError.style.display = 'none';
        alertaExito.style.display = 'block';
        setTimeout(function () {
            alertaExito.style.display = 'none';
        }, 3000);
    }

    function mostrarMensajeError() {
        alertaExito.style.display = 'none';
        alertaError.style.display = 'block';
        setTimeout(function () {
            alertaError.style.display = 'none';
        }, 3000);
    }

});