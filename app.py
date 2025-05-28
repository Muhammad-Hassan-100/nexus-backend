from flask import Flask, request, jsonify
from flask_cors import CORS
from chatllm import chat_response
from university_service import UniversityInfoService

app = Flask(__name__)
CORS(app)

# Initialize University Info Service
university_service = UniversityInfoService()

# Chat endpoint (existing)
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

# University Info API Endpoints

@app.route('/api/university-info', methods=['POST'])
def create_university_info():
    """Create new university information"""
    try:
        data = request.get_json()
        
        if not data or 'category' not in data or 'info' not in data:
            return jsonify({"error": "Category and info are required"}), 400
        
        result = university_service.create_info(data['category'], data['info'])
        
        if result['success']:
            return jsonify(result), 201
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({"error": f"Error creating university info: {str(e)}"}), 500

@app.route('/api/university-info', methods=['GET'])
def get_all_university_info():
    """Get all university information"""
    try:
        result = university_service.get_all_info()
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({"error": f"Error retrieving university info: {str(e)}"}), 500

@app.route('/api/university-info/<int:info_id>', methods=['GET'])
def get_university_info_by_id(info_id):
    """Get university information by ID"""
    try:
        result = university_service.get_info_by_id(info_id)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 404
            
    except Exception as e:
        return jsonify({"error": f"Error retrieving university info: {str(e)}"}), 500

@app.route('/api/university-info/category/<category>', methods=['GET'])
def get_university_info_by_category(category):
    """Get university information by category"""
    try:
        result = university_service.get_info_by_category(category)
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({"error": f"Error retrieving university info: {str(e)}"}), 500

@app.route('/api/university-info/<int:info_id>', methods=['PUT'])
def update_university_info(info_id):
    """Update university information"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided for update"}), 400
        
        category = data.get('category')
        info = data.get('info')
        
        result = university_service.update_info(info_id, category, info)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 404 if "not found" in result['message'] else 400
            
    except Exception as e:
        return jsonify({"error": f"Error updating university info: {str(e)}"}), 500

@app.route('/api/university-info/<int:info_id>', methods=['DELETE'])
def delete_university_info(info_id):
    """Delete university information"""
    try:
        result = university_service.delete_info(info_id)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 404
            
    except Exception as e:
        return jsonify({"error": f"Error deleting university info: {str(e)}"}), 500

@app.route('/api/university-info/search', methods=['GET'])
def search_university_info():
    """Search university information"""
    try:
        query = request.args.get('q', '')
        
        if not query:
            return jsonify({"error": "Search query is required"}), 400
        
        result = university_service.search_info(query)
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({"error": f"Error searching university info: {str(e)}"}), 500

@app.route('/api/university-info/categories', methods=['GET'])
def get_university_categories():
    """Get all unique categories"""
    try:
        result = university_service.get_categories()
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({"error": f"Error retrieving categories: {str(e)}"}), 500

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "message": "University Bot API is running",
        "endpoints": {
            "chat": "/chat",
            "university_info": "/api/university-info",
            "search": "/api/university-info/search",
            "categories": "/api/university-info/categories"
        }
    }), 200

if __name__ == '__main__':
    app.run(debug=True)