from agente_utils import load_checkpointer, State, chatboot_info, get_state, save_checkpointer

from agente_utils import tools

from langgraph.prebuilt import ToolNode

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import StateGraph, START, END

from langchain.schema import SystemMessage, HumanMessage, AIMessage # Esto es necesario para el eval del checkpointer
from langchain_core.messages import ToolMessage

def agent(user_id:str, mensaje:str) -> str:
    
    tool_node = ToolNode(tools)

    workflow = StateGraph(State) # Creo mi grafo con la clase Satate

    workflow.add_node("info", chatboot_info)
    workflow.add_node("tools", tool_node)

    workflow.add_conditional_edges("info", get_state)
    workflow.add_edge("tools", 'info')
    workflow.add_edge(START, "info")

    memory = SqliteSaver.from_conn_string(":memory:")
    
    try:
        checkpointer = load_checkpointer(user_id) # aqui cargo el checkpointer de la DB
    except:
        return 'Lo siento, se ha presentado un problema de conexion, espera unos segundos y vuelveremos a conversar'
    
    if checkpointer is not None:
        #print('if')
        checkpoint, config, metadata = map(eval, checkpointer)

        _ = memory.put(config, checkpoint, metadata)

        graph = workflow.compile(checkpointer=memory)

        graph.update_state(config, checkpoint['channel_values'])
    else:
        #print('else')
        graph = workflow.compile(checkpointer=memory)

    config = {"configurable": {"thread_id": user_id}}

    mensaje_ia = ''
    for event in graph.stream({"messages": ("user", mensaje)}, config=config):
        for value in event.values():
            #print("Assistant:", value["messages"][-1].content)
            mensaje_ia += value["messages"][-1].content + '\n'

    checkpoint = memory.get_tuple(config).checkpoint
    config = memory.get_tuple(config).config
    metadata = memory.get_tuple(config).metadata
    
    save_checkpointer(user_id, checkpoint, config, metadata)

    return mensaje_ia