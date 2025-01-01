
from core.config import config
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langchain_core.tools import tool

#model to run LLM
model = ChatOpenAI(api_key=config.OPENAI_KEY,
                   model="gpt-4o-mini")

#this is the system prompt in langchain 
prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a legal support assistant given a user case story as the users first message. You first analyze the case story and get answers for the following questions if they are not present in the original story. Asks the questions one by one and not in one go.
            You are required to ask the following questions from the user.
    1. "What outcome are you hoping to achieve? For example, are you seeking compensation, holding someone accountable, defending yourself?",
    2. "Please expand on the main issue(s) of the case.",
       
    If the user does not answer any question clearly please ask the question again and explain what the question wants in simpler terms.
    Use the tool checkResponses after the user has answered all the questions correctly. The tool will return True if all the questions have been answered correctly. This tool is only used after asking all the questions from the user.
    """,
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

#this is tool number 1 in langchain
@tool
def get_answer_status(number_questions_answered: int) -> dict:
    """This function returns only if all the required questions in the conversation have been answered."""
    return {"status": number_questions_answered}

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
thread = {"configurable": {"thread_id": "abc123"}}

#get openai response with retries

def get_openai_response(input_conversation):
    try:     
        query = [HumanMessage(input_conversation)]
        response_text= app.invoke({"messages": query}, thread)
        return response_text
    except Exception as e:
        return str(e)


