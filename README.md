# University Bot

A helpful AI assistant designed to answer university-related questions. This bot uses the Llama 3 model from Meta through OpenRouter API.

## Features

- Conversational AI assistant specialized in university topics
- Remembers conversation history for contextual responses
- Simple and easy-to-use interface

## Project Structure

```
backend/
├── app.py             # Main Flask application
├── chatllm.py         # LLM integration with LangChain
├── chroma_db/         # Vector database for document storage
└── __pycache__/       # Python cache files
```

## Setup and Installation

### Prerequisites

- Python 3.8 or higher
- OpenRouter API key

### Installation

1. Clone the repository:
   ```
   git clone <your-repository-url>
   cd "University Bot/backend"
   ```

2. Install the required dependencies:
   ```
   pip install langchain langchain-openai flask
   ```

3. Set up your environment variables (or update them directly in the code):
   ```
   API_KEY = "your-openrouter-api-key"
   ```

## Usage

1. Run the Flask application:
   ```
   python app.py
   ```

2. Send requests to the appropriate endpoint to interact with the bot.

## API Reference

The chatbot can be accessed through:

```
POST /chat
Body: {"user_input": "your question here"}
```

Returns a JSON response with the bot's answer.

## Technology Stack

- [LangChain](https://www.langchain.com/) - Framework for developing applications powered by language models
- [Llama 3](https://ai.meta.com/llama/) - Open-source LLM from Meta
- [OpenRouter](https://openrouter.ai/) - API access to various language models
- Flask - Web framework for the backend API

## License

[MIT License](LICENSE)

## Author

Muhammad Hassan

---

*Note: This project is for educational purposes.*
