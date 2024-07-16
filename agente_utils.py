from typing import Annotated

from typing_extensions import TypedDict

from langgraph.graph import END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage

from typing import Literal

from pymongo import MongoClient

from langchain_core.tools import tool

# Cargar varaible de entorno
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('API_KEY_OPENAI')
uri = os.getenv('URI')


# Metodos para el manejo de las DB
def get_db(registro:str):
    client = MongoClient(uri)
    db = client['usuarios_chat']
    return db[registro]

@tool
def saved_data_user(name: str, phone_number:str, email:str, url_cv:str, url_linkedin:str):
    """Se llama cuando se necesita insertar en base de datos los datos del usuario"""
    collection = get_db('data_users')
    collection.update_one(
        {"phone_number": phone_number},
        {"$set": {
            "name": name,
            "email": email,
            "url_cv": url_cv,
            "url_linkedin": url_linkedin
        }},
        upsert=True
    )

tools = [saved_data_user]


class State(TypedDict):
    messages: Annotated[list, add_messages]

def chatboot_info(state:State):

  template_info = """Eres un asistente virtual. Tu trabajo es obtener información de una persona a la que estas entrevistando.

  Debes obtener la siguiente información de la persona a la que entrevistas:

  - Nombre
  - Numero de Telefono
  - Correo electronico
  - La url donde se pude ver su CV
  - La url donde se pude ver su linkedin

  Cuando solicites la informacion solo debes preguntar por una de ellas, no puedes nunca en una pregunta pedir mas de un dato sea cual sea.

  Cuando el usuario salude diga Hola o algo similar, debes inciar con la primera pregunta.

  Si no logras discernir una información, ¡pídeles que aclaren! No intentes adivinar sin base.

  Si la respuesta del usuario no responde claramente a la pregunta debes volver a preguntar hasta que el usuario responda a la pregunta solicitada con la informacion que se espera.

  Después de poder discernir y tener recopilada toda la información, debes insertar en base de datos los datos recogidos y despedirte, con un mensaje Cordial que al final diga 'Hemos Finalizado'.

  Si ya te has despedido antes e insertado los datos, solo debes responder con la palabra: 'Finalizado', no incluyas nada mas que esta palabra, no debes decirle nunca al usuario que estas almacenando sus datos en una base de datos
  """

  def get_messages_info(messages):
      return [SystemMessage(content=template_info)] + messages

  llm = ChatOpenAI(temperature=0.7, model="gpt-4o", api_key = api_key).bind_tools(tools)

  chain_info = get_messages_info | llm

  return {"messages": [chain_info.invoke(state["messages"])]}


def get_state(state: State):
    messages = state["messages"]

    last_message = messages[-1]

    if last_message.tool_calls:
        return "tools"
    
    return END

# MongoDB

# Función para cargar los datos desde la base de datos
def load_checkpointer(id: str) -> tuple[str, str, str]:

    collection = get_db('state_users')
    document = collection.find_one({"ID":id})

    if document:
        checkpoint = document['checkpoint']
        config = document['config']
        metadata = document['metadata']
        return checkpoint, config, metadata
    
    return None

# Función para guardar los datos en la base de datos
def save_checkpointer(id: str, checkpoint: dict, config: dict, metadata: dict):
    checkpoint, config, metadata = str(checkpoint), str(config), str(metadata)
    collection = get_db('state_users')
    collection.update_one(
        {"ID": id},
        {"$set": {
            "checkpoint": checkpoint,
            "config": config,
            "metadata": metadata
        }},
        upsert=True
    )