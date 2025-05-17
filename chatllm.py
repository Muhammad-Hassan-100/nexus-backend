import os
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

API_KEY = "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"

def read_instruction_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading instruction file {file_path}: {str(e)}")
        return ""

current_dir = os.path.dirname(os.path.abspath(__file__))
do_instructions_path = os.path.join(current_dir, "do_instructions.txt")
dont_instructions_path = os.path.join(current_dir, "dont_instructions.txt")
university_info_path = os.path.join(current_dir, "university_info.txt")

do_instructions = read_instruction_file(do_instructions_path)
dont_instructions = read_instruction_file(dont_instructions_path)
university_info = read_instruction_file(university_info_path)

llm = ChatOpenAI(
    model="meta-llama/llama-3-8b-instruct", 
    api_key=API_KEY,
    openai_api_base="https://openrouter.ai/api/v1"
)

system_message = f"""
You are a helpful assistant for the Federal Urdu University of Arts, Science and Technology (FUUAST). Answer questions about the university and other academic topics.

UNIVERSITY INFORMATION:
{university_info}

BEHAVIOR INSTRUCTIONS:
{do_instructions}

RESTRICTIONS:
{dont_instructions}
"""

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

messages = [
    ("system", system_message),
    ("human", "{question}")
]
prompt_template = ChatPromptTemplate.from_messages(messages)

from langchain.chains import ConversationChain
from langchain_core.prompts import PromptTemplate

conversation_prompt = PromptTemplate.from_template(
    system_message + "\n\n{chat_history}\nHuman: {input}\nAI:"
)

chain = ConversationChain(
    llm=llm,
    prompt=conversation_prompt,
    memory=memory,
    verbose=True
)

def chat_response(user_input):
    if not user_input or not isinstance(user_input, str):
        return "Please provide a valid question."
        
    try:
        response = chain.invoke({"input": user_input})
        
        if isinstance(response, dict) and "response" in response:
            return response["response"]
        else:
            return response
    except Exception as e:
        print(f"Error in chat_response: {str(e)}")
        return "Sorry, I encountered an error. Please try again later."