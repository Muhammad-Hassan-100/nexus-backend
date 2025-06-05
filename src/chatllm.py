import os
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from .database import get_supabase_client

API_KEY = "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"

def read_instruction_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading instruction file {file_path}: {str(e)}")
        return ""

def get_university_info_from_database():
    """Fetch university information from database"""
    try:
        supabase = get_supabase_client()
        result = supabase.table("university_info").select("category, info").order("category").execute()
        
        if result.data:
            university_info = ""
            for item in result.data:
                university_info += f"\n{item['category'].upper().replace('_', ' ')}:\n{item['info']}\n"
            return university_info
        else:
            return "No university information available in database."
    except Exception as e:
        print(f"Error fetching university info from database: {str(e)}")
        return "Error loading university information from database."

current_dir = os.path.dirname(os.path.abspath(__file__))
do_instructions_path = os.path.join(current_dir, "do_instructions.txt")
dont_instructions_path = os.path.join(current_dir, "dont_instructions.txt")

do_instructions = read_instruction_file(do_instructions_path)
dont_instructions = read_instruction_file(dont_instructions_path)
university_info = get_university_info_from_database()

llm = ChatOpenAI(
    model="meta-llama/llama-3-8b-instruct", 
    api_key=API_KEY,
    openai_api_base="https://openrouter.ai/api/v1"
)

system_message = f"""
You are a helpful assistant for Dawood University of Engineering & Technology (DUET). Answer questions about the university and other academic topics.

GREETING RULE: Only respond with greetings (like "Hello", "Hi", "Assalam o Alaikum", etc.) if the user has greeted you first with words like hello, hi, hey, assalam, salam, good morning, etc. Otherwise, directly answer their question without any greeting.

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
        fresh_university_info = get_university_info_from_database()
        greeting_words = ['hello', 'hi', 'hey', 'assalam', 'assalamu alaikum', 'salaam', 'salam', 'good morning', 'good afternoon', 'good evening']
        is_greeting = any(word in user_input.lower() for word in greeting_words)
        
        fresh_system_message = f"""
You are a helpful assistant for Dawood University of Engineering & Technology (DUET). Answer questions about the university and other academic topics.

GREETING RULE: Only respond with greetings (like "Hello", "Hi", "Assalam o Alaikum", etc.) if the user has greeted you first with words like hello, hi, hey, assalam, salam, good morning, etc. Otherwise, directly answer their question without any greeting.

UNIVERSITY INFORMATION:
{fresh_university_info}

BEHAVIOR INSTRUCTIONS:
{do_instructions}

RESTRICTIONS:
{dont_instructions}
"""
        
        fresh_conversation_prompt = PromptTemplate.from_template(
            fresh_system_message + "\n\n{chat_history}\nHuman: {input}\nAI:"
        )
        
        fresh_chain = ConversationChain(
            llm=llm,
            prompt=fresh_conversation_prompt,
            memory=memory,
            verbose=True
        )
        
        response = fresh_chain.invoke({"input": user_input})
        
        if isinstance(response, dict) and "response" in response:
            return response["response"]
        else:
            return response
    except Exception as e:
        print(f"Error in chat_response: {str(e)}")
        return "Sorry, I encountered an error. Please try again later."