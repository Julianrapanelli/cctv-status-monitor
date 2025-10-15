
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

Componente	Tecnología/Herramienta	Descripción
Base de datos	Azure SQL Database	Sistema transaccional. Almacena datos estructurados de dispositivos, sitios, movimientos y eventos
Backend	Python	Lógica de negocio, scripts de ETL y comunicación con la base de datos.
ORM	SQLAlchemy	Manejo de consultas y transacciones a través del mapeo relacional de la base de datos. 
Logging	Módulo logging de Python	Registro de eventos, errores y operaciones críticas
Frontend		

 

2.4 	Modelado de datos
Tabla	Campos relevantes	Restricciones
DISPOSITIVO	IP_ADDRESS, MAC_ADDRESS	UNIQUE, c/ INDEX que permite NULL
DESCONEXION	RECONEXION_DATE	PERMITE NULL, el valor se almacena como NULL por default, cuando el disp. Es reconectado, se realiza UPDATE con fecha de lectura.

 

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

asdfasdfasdfasdfasdfasdfasdf
asdfasdfasdfasdfasdfasdfasdfadf

3.1.1	Provisión de toda la mano de obra especializada y no especializada necesaria incluyendo el pago de las obligaciones que correspondan.

4.	ESPECIFICACIONES TÉCNICAS

	Especificaciones técnicas del sistema.


5.	PRESENTACIÓN DE LAS PROPUESTAS

[]	Los precios cotizados por el oferente no podrán ser modificados por éste una vez presentada la oferta.
[]	Todos los gastos incurridos por el oferente para preparar su oferta, concurrir a la reunión explicativa, realizar la visita a obra, y todo otro gasto de cualquier forma asociado con esta licitación, serán soportados exclusivamente por el oferente, sin reconocimiento alguno por parte de Cofco.
[]	La propuesta económica debe completarse discriminando el Impuesto al Valor Agregado (IVA) en cada precio cotizado.
[]	Los precios ofrecidos serán expresados en $ (pesos de la República Argentina), para los servicios locales y/o materiales de Industria Argentina.
[]	Cualquier otra alternativa y/o variante que desee presentar el oferente en la composición de su oferta, deberá ser presentada por separado y como             alternativa a la solicitada en el párrafo anterior.

6.	INSPECCION Y ENSAYOS
 
	La Dirección de Obra deberá tener libre acceso al taller de fabricación de las estructuras metálicas o de piezas, con el fin de inspeccionar los materiales, la calidad de la mano de obra, controlar el avance de los trabajos y asistir a ensayos cuando se requiera.
	Si durante las inspecciones se comprobara la existencia de materiales, piezas o procedimientos deficientes, el fabricante será el responsable y encargado de corregir tal anormalidad, a su cuenta y costo.
	El hecho que los materiales hubieran sido aceptados en fábrica por la DDO no anula el rechazo final en la obra, si los mismos no se encuentran en las condiciones adecuadas.

7.	PLAZO:
	
	La provisión se deberá completar en un plazo de 30 días a partir de la emisión de la orden de compra.

8.	ENTREGA:

	Se cotizarán los elementos puestos sobre camión en planta COFCO Timbues.

9.	CONDICIONES COMERCIALES 

• MULTA POR INCUMPLIMIENTO DE LOS PLAZOS DE ENTREGA. 
	En caso de mora por incumplimiento de los plazos y condiciones acordados el CONTRATISTA deberá abonar en concepto de multa el 0,5% del monto total del contrato, por cada día de atraso. Dicha multa no podrá exceder del 10 % (Diez por ciento) del valor total del contrato. 
	A los efectos de calcular esta multa se consideran los valores contractuales. 
	La multa se devengará y comenzará a correr en forma automática y de pleno derecho a partir del vencimiento de los plazos comprometidos según oferta acordada y aceptada por Cofco. 
	El CONTRATISTA autoriza expresamente a la PROPIETARIA a retenerle y/o compensarle de los pagos que tenga a percibir, el valor de todas las multas que pudieren surgir durante el proceso de ejecución del presente, como así mismo, a retener cualesquiera de los bienes materiales y/o equipos propiedad del CONTRATISTA que se encuentren en la obra en caso que no existieran fondos suficientes del mismo para hacer frente a la multa adeudada, que, en tal supuesto además la PROPIETARIA estará facultada para percibir judicialmente. 
	Si existieran casos de fuerza mayor no imputables al CONTRATISTA, y que previstos no hubiera podido evitar, para eximirse de las penalidades establecidas, deberá probar fehacientemente, a entera satisfacción del representante técnico que designe la PROPIETARIA, y acreditar en #El Libro de Comunicaciones# las mencionadas razones de fuerza mayor dentro de las 96 hs. de sucedidas. 
	Queda convenido, que en el supuesto caso que se amplíe el plazo de entrega estipulado, ya sea a pedido de cualquiera de las partes, debiendo instrumentarse por escrito fehacientemente, tendiente a la no aplicación de las penalidades a que se refiere la presente cláusula y/o al reconocimiento de mayores costos, no autoriza al reclamo por parte del CONTRATISTA de compensación alguna por ningún concepto. 

• PÓLIZAS DE SEGURO DE CAUCIÓN 
	El CONTRATISTA deberá presentar a la PROPIETARIA, junto con la factura del Anticipo, las siguientes Pólizas de seguro de caución, emitidas por una compañía de seguros de primera línea y a entera satisfacción de Cofco International Argentina S.A.: 
	1 - Por el importe del Anticipo establecido, la que será devuelta en el momento de acordarse la Recepción Provisoria. 
	2 - Por el equivalente al 30 % (treinta)del precio Total mencionado en concepto de Garantía de cumplimiento de las condiciones establecidas en la presente, emitida con vigencia hasta la extinción de las obligaciones del CONTRATISTA, la que será ejecutada por Cofco International Argentina S.A. a las 48 horas de la intimación a regularizar cualquier incumplimiento de nuestra parte. 
	Deberá ser entregado junto con la factura y póliza de caución del anticipo, y será devuelto en el momento de acordarse la recepción provisoria.


