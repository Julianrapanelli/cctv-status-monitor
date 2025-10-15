#Documentación sistema de análisis CCTV



##Índice


###1.- PROPÓSITO	2

###2.- INFORMACIÓN GENERAL DEL SISTEMA	2

###3.- INTERFACES DE USUARIO Y ACCESO 	2

[] [###4.- POLÍTICAS DE USO Y PRIVACIDAD	3]

[] ###5.- FLUJO DE TRABAJO INTERNO Y FUNCIONES	3

[] ###6.- USO	4

[] ###7.- REQUERIMIENTOS Y ESPECIFICACIONES TÉCNICAS 	4


		
 
Especificaciones Técnicas Particulares

1.	PROPÓSITO

	El sistema es una plataforma de gestión de dispositivos diseñada para registrar la ubicación física de dispositivos en sitios y sectores, gestionar movimientos entre ubicaciones (préstamos, devoluciones, traslados) y Monitorear el estado de conexión/desconexión de dispositivos.

2.	INFORMACIÓN GENERAL DEL SISTEMA:
2.1	Capacidades principales del sistema
-	Tanto sistema como base de datos deberán estar alojadas en nube con el fin de asegurar alta disponibilidad.
-	El sistema funciona las 24 horas del día, ejecutando análisis de los dispositivos en la red cada 30 minutos.
-	La interfaz web será accesible desde dispositivos móviles y escritorio.

2.2	Requerimientos principales del sistema
-	El sistema está hecho para trabajar en un entorno cloud que le permita ejecutar determinadas funciones con Python 3.13.
-	La compatibilidad con bases de datos es SQL-Server y el equema de manipulación de datos está orientado a la suite de análisis de Microsoft (Power Apps, Power BI, etc).
-	El sistema en sí no contendrá ninguna credencial ni información del negocio, todo será gestionado de manera transparente y con usuarios determinados a través de Azure Key Vault y Azure SQL.

2.3	Arquitectura del sistema

|     Componente         |     Tecnología/Herramienta        |     Descripción                                                                                               |   |   |
|------------------------|-----------------------------------|---------------------------------------------------------------------------------------------------------------|---|---|
|     Base de   datos    |     Azure SQL   Database          |     Sistema   transaccional. Almacena datos estructurados de dispositivos, sitios,   movimientos y eventos    |   |   |
|     Backend            |     Python                        |     Lógica de   negocio, scripts de ETL y comunicación con la base de datos.                                  |   |   |
|     ORM                |     SQLAlchemy                    |     Manejo de   consultas y transacciones a través del mapeo relacional de la base de datos.                  |   |   |
|     Logging            |     Módulo logging   de Python    |     Registro   de eventos, errores y operaciones críticas                                                     |   |   |
|     Frontend           |                                   |                                                                                                               |   |   |
 

2.4 	Modelado de datos

|     Tabla          |     Campos   relevantes          |     Restricciones                                                                                                                            |   |   |
|--------------------|----------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------|---|---|
|     DISPOSITIVO    |     IP_ADDRESS,   MAC_ADDRESS    |     UNIQUE,   c/ INDEX que permite NULL                                                                                                      |   |   |
|     DESCONEXION    |     RECONEXION_DATE              |     PERMITE   NULL, el valor se almacena como NULL por default, cuando el disp. Es   reconectado, se realiza UPDATE con fecha de lectura.    |   |   |
|                    |                                  |                                                                                                                                              |   |   |
|                    |                                  |                                                                                                                                              |   |   |
|                    |                                  |                                                                                                                                              |   |   |
 

2.5 	Diagrama secuencia de actualización [DESCONEXION]

2.6	Dependencias
-	SQL Server: Versión 2016 o superior.
-	Microsoft ODBC Driver 18 for SQL Server.
-	Python 3.8+ con librerías pandas, SQLAlchemy, pyodbc, dotenv, urllib, logging, icmplib y asyncio.

2.7	Seguridad y privacidad
	Datos sensibles: Los campos de la base de datos que contienen datos importantes para el negocio, como son MAC_ADDRESS e IP_ADDRESS, están encriptados, y con su clave de encriptación alojada en Azure KeyVault.
	Permisos: El acceso a la base de datos está restringido por roles de sólo lectura, administración y servicios.
	Transacciones: El uso de las funciones commit y rollback de la librería SQLAlchemy, permite garantizar consistencia y no afectar integridad de los datos.


3.	INTERFACES DE USUARIO Y ACCESO:

3.1	asdfasdf
