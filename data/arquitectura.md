# Arquitectura del servicio de pedidos

El servicio de pedidos expone una API HTTP construida con FastAPI. PostgreSQL es la fuente de verdad para pedidos, pagos y estados. Redis se usa únicamente como caché de consultas frecuentes; la pérdida de Redis no debe borrar pedidos. Cada pedido recibe un identificador único antes de confirmarse. Las operaciones de escritura usan transacciones para evitar estados parciales. Una transacción de pago fallida deja el pedido pendiente y registra el motivo del rechazo.

La API tiene un endpoint de salud que comprueba el proceso y otro de disponibilidad que verifica la conexión con PostgreSQL. El balanceador sólo envía tráfico a instancias disponibles. Las migraciones del esquema se ejecutan antes de publicar una versión nueva. No se guardan contraseñas ni claves en el código; las credenciales llegan mediante variables de entorno. Los logs registran el identificador de pedido y de solicitud, pero nunca números de tarjeta completos.
