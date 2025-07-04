-- Tabla para manejar secuencias de albaranes
CREATE TABLE IF NOT EXISTS secuencia_albaran (
    anio INTEGER NOT NULL,
    ultimo_numero INTEGER NOT NULL,
    ultima_actualizacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_secuencia_albaran PRIMARY KEY (anio)
);

-- Índice para optimizar búsquedas por año
CREATE INDEX IF NOT EXISTS idx_secuencia_albaran_anio ON secuencia_albaran(anio);

-- Función para obtener y actualizar el siguiente número de albarán
CREATE OR REPLACE FUNCTION obtener_siguiente_numero_albaran()
RETURNS TEXT AS $$
DECLARE
    v_anio INTEGER;
    v_ultimo_numero INTEGER;
    v_siguiente_numero INTEGER;
    v_numero_formateado TEXT;
    v_intentos INTEGER := 0;
    v_max_intentos INTEGER := 3;
BEGIN
    v_anio := EXTRACT(YEAR FROM CURRENT_DATE);
    
    WHILE v_intentos < v_max_intentos LOOP
        -- Intentar obtener o crear el registro para el año actual
        INSERT INTO secuencia_albaran (anio, ultimo_numero, ultima_actualizacion)
        VALUES (v_anio, 0, CURRENT_TIMESTAMP)
        ON CONFLICT (anio) DO UPDATE
        SET ultimo_numero = secuencia_albaran.ultimo_numero + 1,
            ultima_actualizacion = CURRENT_TIMESTAMP
        RETURNING ultimo_numero INTO v_siguiente_numero;

        -- Verificar que el número no exista en cabecera_albaran_ruta
        IF NOT EXISTS (
            SELECT 1 FROM cabecera_albaran_ruta 
            WHERE numero_albaran = v_anio || '/' || LPAD(v_siguiente_numero::TEXT, 3, '0')
        ) THEN
            -- Número válido encontrado
            v_numero_formateado := v_anio || '/' || LPAD(v_siguiente_numero::TEXT, 3, '0');
            RETURN v_numero_formateado;
        END IF;
        
        v_intentos := v_intentos + 1;
    END LOOP;
    
    -- Si llegamos aquí, no pudimos obtener un número único
    RAISE EXCEPTION 'No se pudo obtener un número de albarán único después de % intentos', v_max_intentos;
END;
$$ LANGUAGE plpgsql; 