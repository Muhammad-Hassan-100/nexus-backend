import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
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
    model="google/gemini-2.0-flash-exp:free", 
    api_key=API_KEY,
    openai_api_base="https://openrouter.ai/api/v1"
)

store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful assistant for Dawood University of Engineering & Technology (DUET). Answer questions about the university and other academic topics.

GREETING RULE: Only respond with greetings (like "Hello", "Hi", "Assalam o Alaikum", etc.) if the user has greeted you first with words like hello, hi, hey, assalam, salam, good morning, etc. Otherwise, directly answer their question without any greeting.

RESPONSE GUIDELINES:
- BE CONTEXTUALLY PRECISE: Analyze the exact question and provide the most relevant, specific answer  
- AVOID GENERIC RESPONSES: Different questions require different answers, even about the same topic
- BE DIRECT AND TO-THE-POINT: Give concise but complete answers (2-4 sentences)
- PROVIDE ADEQUATE INFORMATION: Include relevant details without being lengthy
- PROVIDE LOGICAL CALCULATIONS: 
  * For "When established?" questions → Give the year (1962)
  * For "How long established?" questions → Calculate duration (e.g., "63 years since 1962")
  * For duration questions, always calculate from 1962 to current year (2025)

UNIVERSITY INFORMATION:
{university_info}

BEHAVIOR INSTRUCTIONS:
{do_instructions}

RESTRICTIONS:
{dont_instructions}"""),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

chain = chat_prompt | llm | StrOutputParser()

conversational_chain = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)

def chat_response(user_input, session_id="default"):
    if not user_input or not isinstance(user_input, str):
        return "Please provide a valid question."
        
    try:
        fresh_university_info = get_university_info_from_database()
        
        response = conversational_chain.invoke(
            {
                "input": user_input,
                "university_info": fresh_university_info,
                "do_instructions": do_instructions,
                "dont_instructions": dont_instructions
            },
            config={"configurable": {"session_id": session_id}}
        )
        
        return response
    except Exception as e:
        print(f"Error in chat_response: {str(e)}")
        return "Sorry, I encountered an error. Please try again later."