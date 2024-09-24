# Timeout-Unanswered-Messages-in-Genesys-Cloud
Este desarrollo realiza un senso de los mensajes enviados por el usuario mediante en canal de messenger de Genesys Cloud y captura la opción desea para realizar el encolamiento a una queue definida

# Genesys Cloud Message Retrieval API

## Descripción

Esta aplicación web está diseñada para obtener detalles de mensajes de una conversación en Genesys Cloud después de un tiempo específico. Utiliza la API de Genesys Cloud para acceder a la información de las conversaciones y permite identificar interacciones basadas en palabras clave o variaciones específicas en los mensajes del usuario.

### Características principales

- **Autenticación por Organización**: Obtiene tokens de acceso diferentes para cada organización configurada.
- **Obtención de Mensajes**: Recupera mensajes específicos de una conversación a partir de un tiempo determinado.
- **Normalización de Texto**: Permite normalizar el texto de los mensajes para facilitar la comparación con palabras clave predefinidas.
- **Respuesta Detallada**: Devuelve una respuesta indicando si el usuario está interactuando y el mensaje más reciente que coincide con los criterios definidos.

## Requisitos

- Python 3.x
- Librerías necesarias (ver `requirements.txt`):
  - `Flask`
  - `requests`
  - `PureCloudPlatformClientV2`
- Credenciales y permisos necesarios para acceder a las conversaciones en Genesys Cloud.

## Uso

- Inicia la aplicación Flask: `python app_mensajes.py`
- Envía una solicitud POST a `http://localhost:5000/get_message_after` con el siguiente formato JSON:
  `{
  "conversation_id": "ID_de_la_conversacion",
  "after_time": "YYYY-MM-DDTHH:MM:SS.sssZ",
  "organization": "organizacion 1"
}`
- `conversation_id`: ID de la conversación en Genesys Cloud.
- `after_time`: Tiempo en formato ISO 8601 después del cual se desean obtener los mensajes.
- `organization`: Organización para la cual se quiere obtener el token. Puede ser organizacion 1 o organizacion 2.

La respuesta incluirá detalles del último mensaje del usuario después del tiempo especificado, o un mensaje indicando que no hubo interacción.

## Estructura del Proyecto

- `app_mensajes.py`: Script principal que maneja la lógica de la API Flask y la integración con Genesys Cloud.
- `requirements.txt`: Archivo de dependencias necesarias para el proyecto.

## Personalización

- Puedes personalizar las palabras clave y variaciones dentro de la función `get_message_body` para adaptarlas a tu contexto específico.
- Asegúrate de actualizar las credenciales y la configuración de la API en `app_mensajes.py` para conectarte al entorno adecuado de Genesys Cloud.

## Contacto

Si tienes alguna pregunta o sugerencia, no dudes en ponerte en contacto.

- Bryan Ganzen
- 55 75 45 65 81


