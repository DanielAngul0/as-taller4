-- Usuarios (viajeros y aerolíneas)

-- ===========================
-- ESQUEMA DE BASE DE DATOS PARA SERVICIO DE AUTENTICACIÓN (Base de datos: auth_db)
-- ===========================

-- ===========================
-- TABLA DE USUARIOS (Auth Service)
-- ===========================
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(200) NOT NULL,  -- se almacena encriptado
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Datos de prueba
INSERT INTO usuarios (nombre, email, password) VALUES
('Carlos Pérez', 'carlos@example.com', 'hashed_password1'),
('María Gómez', 'maria@example.com', 'hashed_password2'),
('Aerolinea X', 'contacto@aerolineax.com', 'hashed_password3');