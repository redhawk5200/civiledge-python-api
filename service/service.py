from core.config import config
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from db.database import SessionLocal
from db.crud import create_chat_session
from agent.prompts import prompt_template
from agent.tools import get_answer_status

import json

#model to run LLM
model = ChatOpenAI(api_key=config.OPENAI_KEY,
                   model="gpt-4o-mini")

#we are assigning the tools with a list which is having only one tool as of now
tools=([get_answer_status])

#we are binding the tools to the llm model
model_with_tools = model.bind_tools(tools)

# Define a new graph
workflow = StateGraph(state_schema=MessagesState)

def call_model(state: MessagesState):
    prompt = prompt_template.invoke(state)
    response = model_with_tools.invoke(prompt)
    return {"messages": response}

# Define the (single) node in the graph
workflow.add_edge(START, "model")
workflow.add_node("model", call_model)

# Add memory
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

#threads maintain the convo of a user, basically a session_id
# thread = {"configurable": {"thread_id": "abc123"}}

#get openai response with retries

def get_openai_response(input_conversation, userid: str):
    try:     
        query = [HumanMessage(input_conversation)]
        thread_id = f"thread_{userid}"
        thread = {"configurable": {"thread_id": thread_id}}
        
        response_text = app.invoke({"messages": query}, thread)
        
        # Convert messages to a serializable format
        messages_json = json.dumps({
            "input": input_conversation,
            "response": [msg.content for msg in response_text["messages"]]
        })
        
        # Save to database
        db = SessionLocal()
        try:
            create_chat_session(
                db=db,
                userid=userid,
                langchain_thread_id=thread_id,
                messages=messages_json
            )
        finally:
            db.close()

        for message in response_text["messages"]:
            print(message.pretty_print())

        return response_text

    except Exception as e:
        return str(e)
