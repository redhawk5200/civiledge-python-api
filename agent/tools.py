from typing import Annotated
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from agent.prompts import report_format
from core.config import config

@tool
def get_report(
    report: Annotated[str, 
    "The conversation text between user and legal support assistant."]
    ) -> dict:
    """
    Legal summary assistant tool that processes conversation.
    """
    try:
        # Create message content with proper formatting
        content = f"Based on this conversation:\n{report}\n\nGenerate a report following this format:\n{report_format}"
        print("=" * 50)
        # Initialize model
        model = ChatOpenAI(
            api_key=config.OPENAI_KEY,
            model="gpt-4",
            temperature=0
        )
        
        # Create proper message structure
        messages = [AIMessage(content=content)]
        
        # Invoke the model
        response = model.invoke(messages)
        
        # Extract content from response
        report_content = response.content if hasattr(response, 'content') else str(response)
        
        print("=" * 50)
        print("Generated Report:")
        print(report_content)
        print("=" * 50)
        
        return {"report": report_content}
        
    except Exception as e:
        print(f"Error generating report: {str(e)}")
        return {"error": str(e)}