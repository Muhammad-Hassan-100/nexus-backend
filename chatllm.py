import os
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

API_KEY = "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"

# OpenRouter ke liye OpenAI client ko customize karna (api_base change karna)
llm = ChatOpenAI(
    model="meta-llama/llama-3-8b-instruct", 
    api_key=API_KEY,
    openai_api_base="https://openrouter.ai/api/v1"
)

# Create memory for conversation history
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Create a simple prompt template
prompt_template = ChatPromptTemplate.from_template("""
You are a helpful university assistant. Answer questions about university-related topics.
Chat History: {chat_history}
Human: {question}
AI: """
)

# Create a simple chain that uses the prompt template and LLM
from langchain.chains import LLMChain

chain = LLMChain(
    llm=llm,
    prompt=prompt_template,
    memory=memory,
    output_parser=StrOutputParser()
)

def chat_response(user_input):
    # Simple input validation
    if not user_input or not isinstance(user_input, str):
        return "Please provide a valid question."
        
    try:
        # Use the LLM chain to process the input
        response = chain.invoke({"question": user_input})
        return response["text"]  # Return just the text response
    except Exception as e:
        print(f"Error in chat_response: {str(e)}")
        return "Sorry, I encountered an error. Please try again later."