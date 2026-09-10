-- ============================================================
-- sql/esquema.sql
-- Proyecto Integrador U4 - Semana 13
-- Plataforma de Cursos - Modelo relacional mínimo (MySQL)
-- Ejecutar completo en MySQL Workbench (o consola) para recrear
-- la base de datos y sus tablas desde cero.
-- ============================================================

CREATE DATABASE IF NOT EXISTS plataforma_cursos;
USE plataforma_cursos;

-- Tabla Instructores (módulo Proveedores)
CREATE TABLE IF NOT EXISTS instructores (
    id_instructor INT AUTO_INCREMENT PRIMARY KEY,
    nombre        VARCHAR(100) NOT NULL,
    especialidad  VARCHAR(100) NOT NULL,
    correo        VARCHAR(100) NOT NULL
);

-- Tabla Cursos (módulo Productos) - referencia a Instructores
CREATE TABLE IF NOT EXISTS cursos (
    id_curso      INT AUTO_INCREMENT PRIMARY KEY,
    nombre        VARCHAR(100) NOT NULL,
    descripcion   VARCHAR(300) NOT NULL,
    categoria     VARCHAR(50)  NOT NULL,
    precio        DECIMAL(10,2) NOT NULL,
    cupos         INT NOT NULL,
    id_instructor INT NOT NULL,
    FOREIGN KEY (id_instructor) REFERENCES instructores(id_instructor)
);

-- Tabla Estudiantes (módulo Clientes)
CREATE TABLE IF NOT EXISTS estudiantes (
    id_estudiante INT AUTO_INCREMENT PRIMARY KEY,
    nombre        VARCHAR(100) NOT NULL,
    cedula        VARCHAR(20)  NOT NULL,
    telefono      VARCHAR(20),
    correo        VARCHAR(100) NOT NULL
);

-- Tabla Pagos (módulo Facturación) - referencia a Estudiantes y Cursos
CREATE TABLE IF NOT EXISTS pagos (
    id_pago       INT AUTO_INCREMENT PRIMARY KEY,
    id_estudiante INT NOT NULL,
    id_curso      INT NOT NULL,
    monto         DECIMAL(10,2) NOT NULL,
    fecha         DATE NOT NULL,
    FOREIGN KEY (id_estudiante) REFERENCES estudiantes(id_estudiante),
    FOREIGN KEY (id_curso) REFERENCES cursos(id_curso)
);

-- ------------------------------------------------------------
-- Datos semilla de Instructores, necesarios para poder registrar
-- cursos (id_instructor es obligatorio y es FOREIGN KEY).
-- ------------------------------------------------------------
INSERT INTO instructores (nombre, especialidad, correo) VALUES
    ('Ing. Paola Ramirez', 'Frontend y UX/UI', 'paola.ramirez@desarrolloweb.com'),
    ('Ing. Diego Salazar', 'Backend con Python', 'diego.salazar@desarrolloweb.com'),
    ('Ing. Lucia Torres', 'Bases de Datos', 'lucia.torres@desarrolloweb.com');
