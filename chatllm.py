import os
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

API_KEY = "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"

# Function to read instruction files
def read_instruction_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading instruction file {file_path}: {str(e)}")
        return ""

# Read instruction files
current_dir = os.path.dirname(os.path.abspath(__file__))
do_instructions_path = os.path.join(current_dir, "do_instructions.txt")
dont_instructions_path = os.path.join(current_dir, "dont_instructions.txt")

do_instructions = read_instruction_file(do_instructions_path)
dont_instructions = read_instruction_file(dont_instructions_path)

# OpenRouter ke liye OpenAI client ko customize karna (api_base change karna)
llm = ChatOpenAI(
    model="meta-llama/llama-3-8b-instruct", 
    api_key=API_KEY,
    openai_api_base="https://openrouter.ai/api/v1"
)

# Set up the instructions in the system message
system_message = f"""
You are a helpful university assistant. Answer questions about university-related topics.

BEHAVIOR INSTRUCTIONS:
{do_instructions}

RESTRICTIONS:
{dont_instructions}
"""

# Create memory for conversation history
memory = ConversationBufferMemory(memory_key="history", return_messages=True)

# Create a prompt template with the instructions in the system message
# Note: We don't include chat_history as a message type since it's handled by memory
prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_message),
    ("human", "{question}")
])

# Create a chain with the LLM and prompt template
from langchain.chains import LLMChain

chain = LLMChain(
    llm=llm,
    prompt=prompt_template,
    memory=memory,
    output_parser=StrOutputParser(),
    verbose=True  # Add this to see more information for debugging
)

def chat_response(user_input):
    # Simple input validation
    if not user_input or not isinstance(user_input, str):
        return "Please provide a valid question."
        
    try:
        # Use the LLM chain to process the input
        response = chain.invoke({"question": user_input})
        
        # In newer versions of langchain, the response might be just a string
        # rather than a dictionary with a "text" key
        if isinstance(response, dict) and "text" in response:
            return response["text"]
        else:
            return response
    except Exception as e:
        print(f"Error in chat_response: {str(e)}")
        return "Sorry, I encountered an error. Please try again later."