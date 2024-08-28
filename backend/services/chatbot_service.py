from services.request_llm import RequestLLM
from services.prompt_template import PromptTemplate

def get_chatbot_response(question: str) -> str:
    prompt_template = PromptTemplate()
    request_llm = RequestLLM()

    prompt = prompt_template.lawyers(question)

    response = request_llm.request_generate(prompt)
    response = str(response) 
    
    return response.strip()