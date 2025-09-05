-- Pagos y facturación

-- ===========================
-- ESQUEMA DE BASE DE DATOS PARA EL SERVICIO DE PAGOS (Base de datos: pagos_db)
-- ===========================

-- ===========================
-- TABLA DE PAGOS (Pagos Service)
-- ===========================
CREATE TABLE pagos (
    id SERIAL PRIMARY KEY,
    usuario_id INT NOT NULL,
    reserva_id INT NOT NULL,
    monto DECIMAL(10,2) NOT NULL,
    metodo_pago VARCHAR(50) NOT NULL,
    estado VARCHAR(20) NOT NULL DEFAULT 'pendiente', -- pendiente, aprobado, rechazado
    fecha_pago TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Datos de prueba
INSERT INTO pagos (usuario_id, reserva_id, monto, metodo_pago, estado) VALUES
(1, 1, 250.00, 'tarjeta_credito', 'aprobado'),
(2, 2, 180.00, 'paypal', 'pendiente'),
(1, 3, 120.00, 'tarjeta_debito', 'rechazado');