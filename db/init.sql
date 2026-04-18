-- 1. Activamos la extensión de mapas
CREATE EXTENSION IF NOT EXISTS postgis;

-- 2. Creamos la tabla de Puntos de Interés
CREATE TABLE IF NOT EXISTS puntos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    descripcion TEXT,
    categoria VARCHAR(50),
    ubicacion GEOGRAPHY(Point, 4326) -- Aquí se guarda la magia geoespacial
);

-- 3. Insertamos los 5 puntos de ejemplo (Seeding)
INSERT INTO puntos (nombre, descripcion, categoria, ubicacion) VALUES
('Torre Eiffel', 'Monumento en París', 'Cultural', ST_GeogFromText('POINT(2.2945 48.8584)')),
('Estatua de la Libertad', 'Monumento en NY', 'Cultural', ST_GeogFromText('POINT(-74.0445 40.6892)')),
('Gasolinera Central', 'Servicio 24h', 'Servicios', ST_GeogFromText('POINT(-3.7038 40.4168)')),
('Restaurante El Faro', 'Comida de mar', 'Gastronomía', ST_GeogFromText('POINT(-12.1252 -77.0305)')),
('Parque Nacional', 'Reserva natural', 'Natural', ST_GeogFromText('POINT(-68.3030 -54.8019)'));