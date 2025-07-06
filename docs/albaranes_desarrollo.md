# Desarrollo del Sistema de Albaranes

## Estructura de la Tabla lineas_albaran_ruta

| CAMPOS | DESCRIPCIONES |
|--------|---------------|
| id | pk |
| cabecera_id | fk |
| fecha_albaran | fecha seleccionada en la cabecera |
| num_alb_ruta | numero correspondiente a la cabecera |
| serie_alb | viene de la consulta sql debe ser tipo texto |
| fecha_alb | viene de la consulta sql |
| numero_alb | viene de la consulta sql debe ser tipo texto |
| nombre_cliente | viene de la consulta sql debe ser tipo texto |
| cod_cliente | viene de la consulta sql debe ser tipo texto |
| municipio_envio | viene de la consulta sql debe ser tipo texto |
| importe | viene de la consulta sql |
| beneficio | viene de la consulta sql |
| imp_liqu | viene de la consulta sql |
| porcentaje | viene de la consulta sql |
| conductor | viene de la consulta sql |
| tlpa | campo calculado obtenido del campo 'importe' multiplicado por el campo 'porcentaje_pactado' ejemplo: 'importe'=100 'porcentaje pactado'=4 entonces 100*0.04 |
| ben_post_log | campo calculado de la resta de 'beneficio' menos 'tlpa' |
| por_ben_real | campo calculado dividiendo campo 'ben_post_log' sobre 'importe' |
| deuda | viene de la consulta sql |
| lineas | viene de la consulta sql |
| fecha_registro | fecha y hora en la que se registra el dato en la base de datos por un usuario (inmodificable) |

## Consulta SQL Server para Obtener Datos

```sql
SELECT 
    CONCAT(a.SerieAlbaran, a.NumeroAlbaran) AS ALBARAN,
    a.RazonSocial,
    a.CodigoCliente,
    a.MunicipioEnvios,
    a.ImporteLiquido,
    a.FechaAlbaran,
    a.MargenBeneficio,
    a.PorMargenBeneficio,
    t.Transportista,
    a.BaseImponible,
    a.NumeroLineas,
    deuda_table.deuda
FROM [MMARKET].[dbo].[CabeceraAlbaranCliente] a
LEFT JOIN Transportistas t 
    ON t.CodigoEmpresa = a.CodigoEmpresa 
    AND t.CodigoTransportista = a.CodigoTransportistaEnvios
LEFT JOIN (
    SELECT 
        CodigoClienteProveedor,
        CONCAT(FORMAT(SUM(ImporteEfecto), 'N2', 'es-ES'), '€') AS deuda
    FROM CarteraEfectos
    WHERE CodigoEmpresa = 1
        AND Prevision = 'C'
        AND StatusBorrado = 0
    GROUP BY CodigoClienteProveedor
) AS deuda_table 
    ON deuda_table.CodigoClienteProveedor = a.CodigoCliente
WHERE a.CodigoEmpresa = 1
    AND a.Ejercicioalbaran > 2023
```

## Funcionalidad Implementada

1. Interfaz de usuario:
   - Formulario tipo Excel para líneas de albarán
   - Solo se ingresan manualmente `serie_alb` y `numero_alb`
   - Los demás campos se autocompletarán con datos de SQL Server
   - Campo `importe` es editable con confirmación
   - Botones OK y Más para finalizar líneas

2. Características:
   - Cache de resultados SQL Server
   - Cálculos automáticos de campos dependientes
   - Actualización de totales en cabecera
   - Validación de campos completos

## Preguntas y Respuestas de Implementación

Q: ¿La consulta SQL debe ejecutarse cada vez o cachear resultados?
A: Mejor cachear los resultados.

Q: Para el campo importe modificable, ¿debe recalcular campos dependientes?
A: Sí, debe recalcular automáticamente los campos dependientes.

Q: ¿El mensaje de alerta para modificar importe?
A: Debe ser un mensaje de confirmación/cancelación, explicando que se recalcularán campos dependientes.

Q: ¿Los botones OK y Más deben estar habilitados solo con campos llenos?
A: Sí, para evitar líneas incompletas.

## Próximos Pasos

1. Implementar guardado de líneas en PostgreSQL
2. Completar cálculos de cabecera
3. Implementar validaciones adicionales
4. Pruebas de integración 