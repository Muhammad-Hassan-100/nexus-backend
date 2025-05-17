from flask import Flask, request, jsonify
from flask_cors import CORS
from chatllm import chat_response

app = Flask(__name__)
CORS(app)

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    try:
        response = chat_response(user_input)
        return jsonify({"response": response})
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        return jsonify({"error": "An error occurred processing your request. Please try again."}), 500

if __name__ == '__main__':
    app.run(debug=True)