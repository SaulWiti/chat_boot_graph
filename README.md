# Proyecto de Chatbot con FastAPI y LangGraph

Este proyecto implementa un chatbot utilizando FastAPI y LangGraph. El chatbot puede mantener una conversación con el usuario, utilizando herramientas y guardando estados en una base de datos SQLite.

## Requisitos

- Python 3.8+
- FastAPI
- LangGraph
- MongoDB
- Otros requerimientos especificados en el archivo `requirements.txt`

## Estructura del Proyecto

- `main.py`: Contiene la configuración de la API con FastAPI.
- `agente.py`: Implementa la lógica del chatbot.
- `agente_utils.py`: Contiene funciones auxiliares y herramientas utilizadas por el chatbot.
- `.env`: Archivo de configuración con variables de entorno.
- `probar_api.ipynb`: Notebook para probar los endpoints de la API.
- `prueba.ipynb`: Notebook para interactuar con el chatbot.

## Instalación

1. Clonar el repositorio:
    ```sh
    git clone <URL del repositorio>
    cd <nombre del repositorio>
    ```

2. Crear y activar un entorno virtual:
    ```sh
    python -m venv env
    source env/bin/activate  # En Windows: .\env\Scripts\activate
    ```

3. Instalar las dependencias:
    ```sh
    pip install -r requirements.txt
    ```

4. Configurar las variables de entorno. Crear un archivo `.env` en la raíz del proyecto con el siguiente contenido:
    ```
    API_KEY_OPENAI = 'tu_api_key_openai'
    API_KEY_AUTH = 'chat1234'
    URI = "mongodb+srv://s*u**iaz:****@userchat.amohfjz.mongodb.net/?retryWrites=true&w=majority&appName=UserChat"
    ```


### Interacción con el Chatbot

1. Probar el chatbot con `prueba.ipynb`:
    - Abre el notebook `prueba.ipynb` con Jupyter Notebook.
    - Ejecuta las celdas para interactuar con el chatbot.

Debe de poner un user_id de un numero de telefono que no se halla usado, no tiene ninguna validacion por el momento.
Para dejar de interactuar pulse q o Q

```python
from agente import agent

user_id = '+5355555555'

while True:
    user_input = input("User: ")
    print('User:', user_input)

    if user_input in ['q', 'Q']:
        break
    else:
        print('Assistant:', agent(user_id, user_input))
```

## Prueba de la api

1. Iniciar la aplicación:
    ```sh
    uvicorn main:app --reload
    ```

2. Probar la API con `probar_api.ipynb`:
    - Abre el notebook `probar_api.ipynb` con Jupyter Notebook.
    - Ejecuta las celdas para probar los endpoints de la API.

## Endpoints

### POST /chatbot
Este endpoint recibe un mensaje del usuario y devuelve una respuesta del chatbot.

- **URL**: `/chatboot`
- **Método HTTP**: `POST`
- **Headers**: `api-key-auth`
- **Body**:
    ```json
    {
        "id_user": "+12345678",
        "sms_user": "Hola"
    }
    ```

- **Respuesta**:
    ```json
    {
        "sms_asistant": "Necesito la URL donde se puede ver tu CV, por favor."
    }
    ```

## Ejemplo de Uso

### Código para Probar la API
```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

peticion = {
    "id_user": '+12345678',
    "sms_user": 'Hola'
}

headers = {
    "api-key-auth": 'chat1234'
}

def test_analizar():
    response = client.post("/chatboot", json=peticion, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "sms_asistant" in data
    print("Resultado de la API:\n", data)

test_analizar()
```
