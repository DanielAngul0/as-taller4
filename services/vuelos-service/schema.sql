-- Vuelos (rutas, horarios, aeronaves, asientos)

-- ===========================
-- ESQUEMA DE BASE DE DATOS PARA EL SERVICIO DE VUELOS (Base de datos: vuelos_db)
-- ===========================

-- ===========================
-- TABLA DE VUELOS (Vuelos Service)
-- ===========================
CREATE TABLE vuelos (
    id SERIAL PRIMARY KEY,
    aerolinea VARCHAR(100) NOT NULL,
    origen VARCHAR(50) NOT NULL,
    destino VARCHAR(50) NOT NULL,
    fecha_salida TIMESTAMP NOT NULL,
    fecha_llegada TIMESTAMP NOT NULL,
    aeronave VARCHAR(50),
    precio NUMERIC(10,2) NOT NULL CHECK (precio >= 0),
    asientos_disponibles INT NOT NULL CHECK (asientos_disponibles >= 0)
);

-- ===========================
-- DATOS DE PRUEBA
-- ===========================
INSERT INTO vuelos (aerolinea, origen, destino, fecha_salida, fecha_llegada, aeronave, precio, asientos_disponibles) VALUES
('Aerolinea X', 'Bogotá', 'Medellín', '2025-09-10 08:00:00', '2025-09-10 09:00:00', 'Airbus A320', 250000, 50),
('Aerolinea X', 'Medellín', 'Cartagena', '2025-09-11 10:00:00', '2025-09-11 11:30:00', 'Boeing 737', 300000, 30),
('Aerolinea Y', 'Bogotá', 'Miami', '2025-09-12 15:00:00', '2025-09-12 19:00:00', 'Airbus A330', 1200000, 100);
