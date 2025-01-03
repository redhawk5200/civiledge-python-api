from langchain_core.tools import tool


#this is tool number 1 in langchain
@tool
def get_answer_status(number_questions_answered: int) -> dict:
    """This function returns only if all the required questions in the conversation have been answered."""
    return {"status": number_questions_answered}