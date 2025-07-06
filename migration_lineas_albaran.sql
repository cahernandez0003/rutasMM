-- Renombrar columnas existentes
ALTER TABLE lineas_albaran_ruta 
    RENAME COLUMN numero_albaran TO numero_alb;

ALTER TABLE lineas_albaran_ruta 
    RENAME COLUMN codigo_cliente TO cod_cliente;

ALTER TABLE lineas_albaran_ruta 
    RENAME COLUMN importe_liquido_linea TO imp_liqu;

ALTER TABLE lineas_albaran_ruta 
    RENAME COLUMN ilpa TO tlpa;

ALTER TABLE lineas_albaran_ruta 
    RENAME COLUMN beneficio_menos_log TO ben_post_log;

ALTER TABLE lineas_albaran_ruta 
    RENAME COLUMN beneficio_real TO por_ben_real;

ALTER TABLE lineas_albaran_ruta 
    RENAME COLUMN deuda_cliente TO deuda;

-- Agregar nuevas columnas
ALTER TABLE lineas_albaran_ruta 
    ADD COLUMN num_alb_ruta text,
    ADD COLUMN serie_alb text;

-- Modificar tipos de datos para ajustar a la nueva estructura
ALTER TABLE lineas_albaran_ruta 
    ALTER COLUMN importe TYPE numeric(10,2),
    ALTER COLUMN beneficio TYPE numeric(10,2),
    ALTER COLUMN imp_liqu TYPE numeric(10,2),
    ALTER COLUMN porcentaje TYPE numeric(5,2),
    ALTER COLUMN tlpa TYPE numeric(10,2),
    ALTER COLUMN ben_post_log TYPE numeric(10,2),
    ALTER COLUMN por_ben_real TYPE numeric(10,2),
    ALTER COLUMN deuda TYPE numeric(10,2);

-- Eliminar columnas que ya no se necesitan
ALTER TABLE lineas_albaran_ruta 
    DROP COLUMN descuento_pronto_pago,
    DROP COLUMN firma_recibe;

-- Actualizar las restricciones de NOT NULL según sea necesario
ALTER TABLE lineas_albaran_ruta 
    ALTER COLUMN numero_alb DROP NOT NULL;

-- Actualizar los índices
DROP INDEX IF EXISTS idx_lineas_numero_albaran;
CREATE INDEX idx_lineas_numero_alb ON lineas_albaran_ruta(numero_alb);

-- Separar el número de albarán en serie y número
UPDATE lineas_albaran_ruta 
SET serie_alb = SUBSTRING(numero_alb FROM '^[A-Za-z]+'),
    num_alb_ruta = numero_alb
WHERE numero_alb IS NOT NULL; 