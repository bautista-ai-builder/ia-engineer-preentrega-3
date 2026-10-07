# Operación y recuperación

PostgreSQL crea un respaldo completo cada noche a las 02:00 UTC y conserva siete copias. El equipo comprueba la restauración una vez por mes en un entorno aislado. El objetivo de recuperación es cuatro horas y la pérdida de datos tolerada es de veinticuatro horas. Antes de restaurar, el operador comunica el incidente, identifica el último respaldo válido y congela escrituras para evitar cambios divergentes.

Redis puede reiniciarse sin restaurar un respaldo porque funciona como caché. Después de un reinicio, la aplicación rellena las entradas desde PostgreSQL. Si la base de datos no responde, el servicio deja de aceptar operaciones de escritura y devuelve un error temporal. El operador revisa conexiones, almacenamiento y logs antes de reanudar tráfico. Una vez recuperada la base, ejecuta una consulta de consistencia sobre pedidos pendientes y compara los totales del día.
