# H1 - Mi proceso lento: búsqueda de huéspedes en el hostal

El proceso que quiero optimizar es la búsqueda de un huésped en el registro del Hostal Kantu Flor, en Copacabana. 
El hostal tiene 20 habitaciones (de la 50 a la 69, repartidas en tres pisos y una terraza) y registra todo a mano en una 
"Hoja diaria de hospedaje". Cada día se llena una hoja nueva con una fila por habitación: número, tipo, nombre del huésped,
precio, cantidad de huéspedes, tiempo de estadía, garage, pago en efectivo, pago por QR y si ya canceló.


El problema aparece cuando hay que encontrar a un huésped. Por ejemplo, cuando alguien que ya se hospedó vuelve porque
olvidó un objeto y hay que saber en qué habitación y en qué fechas estuvo. También pasa al buscar una reserva por nombre o por documento.


Lo sufren sobre todo el recepcionista, que debe revisar hoja por hoja, y el huésped, que espera mientras tanto. Como las hojas solo están 
ordenadas por fecha y no por nombre, la búsqueda es secuencial: hay que mirar todas las filas de todas las hojas hasta encontrar al huésped.


El volumen de datos cambia según la temporada: hay días con 6 habitaciones ocupadas y otros en que el hostal se llena.
Estimo varias hojas al año, con cientos de filas ocupadas acumuladas.

Hoy encontrar a un huésped toma aproximadamente 10 minutos si la estadía fue la semana pasada, y hasta 30 minutos o más si fue hace meses. 
Mi objetivo en este curso es reemplazar esa búsqueda secuencial por una estructura ordenada o indexada que permita encontrarlo en segundos.

