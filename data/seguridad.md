# Seguridad y acceso

El acceso administrativo exige autenticación multifactor. Los permisos se asignan por rol: soporte puede leer el estado de un pedido, operaciones puede revisar métricas y administradores pueden cambiar configuraciones. Ningún rol de lectura puede modificar pagos. Los tokens de acceso vencen a los treinta minutos y se transmiten sólo mediante HTTPS. Las claves de servicios se almacenan en un gestor de secretos y se rotan cada noventa días.

Los eventos de autenticación fallida se registran con hora, identificador de usuario y origen de red. Los logs operativos se conservan treinta días. Un incidente que involucre exposición de datos debe escalarse al responsable de seguridad inmediatamente. El equipo debe revocar credenciales comprometidas, preservar evidencia y revisar el alcance antes de habilitar nuevamente el acceso. Las copias de seguridad se cifran en reposo y su restauración requiere una cuenta separada de la utilizada por la aplicación.
