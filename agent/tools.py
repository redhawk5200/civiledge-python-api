from langchain_core.tools import tool


#this is tool number 1 in langchain
@tool
def get_summary(report: str) -> dict:
    """
    You are a legal summary assistant. You have been given a conversation between the user and the legal support assistant.
            The conversation contains the the user's case story and a set of questions asked by the legal support assistant, to which the user has responded. 
            Your task is to extract the case story, questions asked by the legal support assistant and the user's relevant responses in the following format:

            Case Story:
            
            [Case Story]

            Questions Asked:

            Question 1: [Question 1]
            Answer 1: [Answer 1]

            Question 2: [Question 2]
            Answer 2: [Answer 2]

            and so on for all the questions asked by the legal support assistant and the user's responses.

            Dont repeat the question and answer, first is the case story, then one question followed by one answer.

            Once you have extracted the information, you will return the extracted information as the response to the user.
"""
    return {"report": report}