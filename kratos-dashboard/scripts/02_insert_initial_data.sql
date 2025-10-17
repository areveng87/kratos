USE KratosDB;
GO

-- Insertar roles
INSERT INTO ROLES (nombre, descripcion) VALUES 
('Administrador', 'Acceso completo al sistema'),
('Analista PBC', 'Análisis de operaciones PBC'),
('OCI Interno', 'Operaciones internas OCI'),
('OCI Externo', 'Operaciones externas OCI'),
('SPV', 'Gestión de vehículos especiales'),
('Servicer Supervisor', 'Supervisión de servicios'),
('Servicer Operador', 'Operación de servicios'),
('Auditor', 'Auditoría y revisión');

-- Insertar usuario administrador por defecto
-- Password: admin123 (hasheado con bcrypt)
INSERT INTO USUARIOS (email, password_hash, nombre, apellido, rol_id) VALUES 
('admin@kratos.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBdXwtO5S7ZQJi', 'Admin', 'Sistema', 1);

-- Insertar empresas de ejemplo
INSERT INTO EMPRESAS (nombre, rut, direccion, telefono, email) VALUES 
('Muebles del Sur S.A.', '96.123.456-7', 'Av. Principal 123, Santiago', '+56912345678', 'contacto@mueblesdelsur.cl'),
('Decoraciones Norte Ltda.', '76.987.654-3', 'Calle Comercio 456, Antofagasta', '+56987654321', 'ventas@decoracionesnorte.cl'),
('Furniture Express SpA', '77.555.888-9', 'Av. Libertad 789, Valparaíso', '+56955588899', 'info@furnitureexpress.cl');

-- Insertar operaciones de ejemplo
INSERT INTO OPERACIONES (empresa_id, usuario_id, tipo_operacion, monto, estado, descripcion) VALUES 
(1, 1, 'COMPRA', 150000.00, 'COMPLETADA', 'Adquisición de muebles de oficina'),
(2, 1, 'VENTA', 85000.00, 'PENDIENTE', 'Venta de decoraciones navideñas'),
(3, 1, 'COMPRA', 220000.00, 'EN_PROCESO', 'Importación de muebles europeos'),
(1, 1, 'VENTA', 95000.00, 'COMPLETADA', 'Venta de escritorios ejecutivos'),
(2, 1, 'COMPRA', 180000.00, 'COMPLETADA', 'Compra de materiales decorativos');
