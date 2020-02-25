# Whatsapp API

El objetivo de este proyecto es crear una API que analice las conversaciones de un chat. Para su desarrollo, se ha hecho uso de un grupo de Whatsapp real.

A continuación se indican los pasos a seguir y las funcionalidades:

### 1.- OBTENCIÓN DE LOS DATOS

Descarga de un fichero .txt desde la aplicación de Whatsapp del grupo o conversación que queramos analizar. Esto se puede conseguir desde la opción `Exportar chat` en el apartado `Más` del menú desplegable.

![](https://github.com/Shurlena/whatsapp-API/blob/master/images/whatsapp-file.png)

### 2.- LIMPIEZA DE DATOS

El fichero descargado es necesario limpiarlo y adaptarlo al formato correcto para poder tratar los datos. Este proceso se realiza en el fichero `dataCleaning.py`.

### 3.- CREACION BASE DE DATOS

Una vez nuestros datos estén preparados, podemos crear nuestra base de datos con los usuarios que participan en el grupo, los chats (en este caso, se ha considerado cada día un chat independiente debido a la elevada cantidad de mensajes por día) y las conversaciones o mensajes que ha escrito cada usuario. Esto se traduce en tres colecciones diferentes cuyo aspecto en MongoDB es el siguiente:

![](https://github.com/Shurlena/whatsapp-API/blob/master/images/apichat-mongodb.png)

En la API (`api.py`) se reunen todas estas acciones bajo una única función que se llamará con la ruta `/createdatabase`

### 4.- PETICIONES [POST]

Es posible añadir información adicional a nuestra base de datos, como:

- Crear un usuario: `/insert/user/<name>`
- Crear un chat: `/insert/chat/<name>`
- Creat un mensaje: `/insert/message/<chat>/<name>/<datetime>/<message>`
- Insertar un usuario en un chat: `/insert/user/to/chat/<chat>/<name>`

### 5.- PETICIONES [GET]

Y, finalmente, podemos obtener información sobre el chat mediante la API. Las opciones disponibles hasta ahora son:

- Lista con todos los participantes: `/get/info/users`
- Lista con todos los chats: `/get/info/chats`
- Todos los mensajes de un chat: `/get/info/<chat>`
- Mensajes escritos por un usuario: `/get/messages/<name>`
- Análisis de sentimientos de un chat (método 1): `/get/sentiments/from/<chat>`
- Análisis de sentimientos de un chat (método 2): `/get/sentiments/from/spanish/<chat>`
- Recomendación de usuarios similares: `/recommend/user/<name>`

** El desglose del funcionamiento de cada posible petición se encuentra más desarrollado dentro de cada fichero .py pertinente.

** En el fichero `api-tests.ipynb` se pueden ver los resultados que arroja cada una de las peticiones.