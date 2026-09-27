-- ============================================================
-- sql/esquema.sql
-- Proyecto Integrador U4 - Semana 15
-- Plataforma de Cursos - Modelo relacional (PostgreSQL)
--
-- IMPORTANTE: a diferencia de MySQL, PostgreSQL no permite crear
-- la base de datos dentro del mismo script que crea sus tablas.
-- Primero cree la base "plataforma_cursos" (en pgAdmin, psql, o
-- automáticamente si usa la base que Render ya le entregó) y luego
-- ejecute el resto de este script conectado a esa base.
-- ============================================================

-- Ejecutar solo en local, con un superusuario (psql -U postgres):
-- CREATE DATABASE plataforma_cursos;
-- \c plataforma_cursos

-- Tabla Instructores (módulo Proveedores)
CREATE TABLE IF NOT EXISTS instructores (
    id_instructor SERIAL PRIMARY KEY,
    nombre        VARCHAR(100) NOT NULL,
    especialidad  VARCHAR(100) NOT NULL,
    correo        VARCHAR(100) NOT NULL
);

-- Tabla Cursos (módulo Productos) - referencia a Instructores
CREATE TABLE IF NOT EXISTS cursos (
    id_curso      SERIAL PRIMARY KEY,
    nombre        VARCHAR(100) NOT NULL,
    descripcion   VARCHAR(300) NOT NULL,
    categoria     VARCHAR(50)  NOT NULL,
    precio        DECIMAL(10,2) NOT NULL,
    cupos         INT NOT NULL,
    id_instructor INT NOT NULL REFERENCES instructores(id_instructor)
);

-- Tabla Estudiantes (módulo Clientes)
CREATE TABLE IF NOT EXISTS estudiantes (
    id_estudiante SERIAL PRIMARY KEY,
    nombre        VARCHAR(100) NOT NULL,
    cedula        VARCHAR(20)  NOT NULL,
    telefono      VARCHAR(20),
    correo        VARCHAR(100) NOT NULL
);

-- Tabla Pagos (módulo Facturación) - referencia a Estudiantes y Cursos
CREATE TABLE IF NOT EXISTS pagos (
    id_pago       SERIAL PRIMARY KEY,
    id_estudiante INT NOT NULL REFERENCES estudiantes(id_estudiante),
    id_curso      INT NOT NULL REFERENCES cursos(id_curso),
    monto         DECIMAL(10,2) NOT NULL,
    fecha         DATE NOT NULL
);

-- Tabla Usuarios (Semana 14) - sistema de autenticación (login)
-- La contraseña nunca se guarda en texto plano: se transforma con
-- generate_password_hash() antes del INSERT (ver forms/usuario_form.py
-- y la ruta /registro en app.py).
CREATE TABLE IF NOT EXISTS usuarios (
    id       SERIAL PRIMARY KEY,
    usuario  VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- ------------------------------------------------------------
-- Datos semilla de Instructores, necesarios para poder registrar
-- cursos (id_instructor es obligatorio y es FOREIGN KEY).
-- Se usa ON CONFLICT para poder re-ejecutar el script sin duplicar filas.
-- ------------------------------------------------------------
INSERT INTO instructores (nombre, especialidad, correo) VALUES
    ('Ing. Paola Ramirez', 'Frontend y UX/UI', 'paola.ramirez@desarrolloweb.com'),
    ('Ing. Diego Salazar', 'Backend con Python', 'diego.salazar@desarrolloweb.com'),
    ('Ing. Lucia Torres', 'Bases de Datos', 'lucia.torres@desarrolloweb.com')
ON CONFLICT DO NOTHING;
