from flask import Flask, request, jsonify
from flask_cors import CORS
from chatllm import chat_response
from university_service import UniversityInfoService
import os
from database import get_supabase_client

app = Flask(__name__)
CORS(app)

university_service = UniversityInfoService()

supabase = get_supabase_client()


@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login endpoint"""
    try:
        data = request.get_json()

        if not data or 'username' not in data or 'password' not in data:
            return jsonify({
                "success": False,
                "message": "Username and password are required"
            }), 400

        username = data['username']
        password = data['password']

        try:
            result = supabase.table('credentials').select('*').limit(
                1).execute()
        except Exception:
            try:
                default_credentials = [{
                    "username": "admin",
                    "password": "admin123"
                }, {
                    "username": "duet_admin",
                    "password": "duet2024"
                }, {
                    "username": "superuser",
                    "password": "super123"
                }]
                supabase.table('credentials').insert(
                    default_credentials).execute()
            except Exception as create_error:
                print(f"Error creating credentials table: {create_error}")

        result = supabase.table('credentials').select('id, username').eq(
            'username', username).eq('password', password).execute()

        if result.data and len(result.data) > 0:
            user = result.data[0]
            return jsonify({
                "success": True,
                "message": "Login successful",
                "user": {
                    "id": user['id'],
                    "username": user['username']
                }
            }), 200
        else:
            return jsonify({
                "success": False,
                "message": "Invalid credentials"
            }), 401

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Login error: {str(e)}"
        }), 500


@app.route('/api/auth/update-credentials', methods=['PUT'])
def update_credentials():
    """Update username and password"""
    try:
        data = request.get_json()

        if not data or 'current_username' not in data or 'current_password' not in data:
            return jsonify({
                "success": False,
                "message": "Current credentials are required"
            }), 400

        current_username = data['current_username']
        current_password = data['current_password']
        new_username = data.get('new_username', current_username)
        new_password = data.get('new_password', current_password)

        result = supabase.table('credentials').select('id').eq(
            'username', current_username).eq('password',
                                             current_password).execute()

        if not result.data or len(result.data) == 0:
            return jsonify({
                "success": False,
                "message": "Invalid current credentials"
            }), 401

        user_id = result.data[0]['id']

        update_result = supabase.table('credentials').update({
            'username':
            new_username,
            'password':
            new_password
        }).eq('id', user_id).execute()

        return jsonify({
            "success": True,
            "message": "Credentials updated successfully"
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Update error: {str(e)}"
        }), 500


@app.route('/api/auth/get-credentials', methods=['POST'])
def get_credentials():
    """Get current credentials for a user"""
    try:
        data = request.get_json()

        if not data or 'username' not in data:
            return jsonify({
                "success": False,
                "message": "Username is required"
            }), 400

        username = data['username']

        result = supabase.table('credentials').select('username, password').eq(
            'username', username).execute()

        if result.data and len(result.data) > 0:
            credentials = result.data[0]
            return jsonify({
                "success": True,
                "message": "Credentials retrieved successfully",
                "credentials": credentials
            }), 200
        else:
            return jsonify({
                "success": False,
                "message": "User not found"
            }), 404

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Get credentials error: {str(e)}"
        }), 500


@app.route('/api/auth/get-all-credentials', methods=['GET'])
def get_all_credentials():
    """Get all credentials from database"""
    try:
        result = supabase.table('credentials').select(
            'username, password').execute()

        if result.data and len(result.data) > 0:
            return jsonify({
                "success": True,
                "message": "Credentials retrieved successfully",
                "credentials": result.data
            }), 200
        else:
            return jsonify({
                "success": False,
                "message": "No credentials found in database"
            }), 404

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Get all credentials error: {str(e)}"
        }), 500


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
        return jsonify({
            "error":
            "An error occurred processing your request. Please try again."
        }), 500


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
        return jsonify({"error":
                        f"Error creating university info: {str(e)}"}), 500


@app.route('/api/university-info', methods=['GET'])
def get_all_university_info():
    """Get all university information"""
    try:
        result = university_service.get_all_info()
        return jsonify(result), 200

    except Exception as e:
        return jsonify(
            {"error": f"Error retrieving university info: {str(e)}"}), 500


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
        return jsonify(
            {"error": f"Error retrieving university info: {str(e)}"}), 500


@app.route('/api/university-info/category/<category>', methods=['GET'])
def get_university_info_by_category(category):
    """Get university information by category"""
    try:
        result = university_service.get_info_by_category(category)
        return jsonify(result), 200

    except Exception as e:
        return jsonify(
            {"error": f"Error retrieving university info: {str(e)}"}), 500


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
            return jsonify(
                result), 404 if "not found" in result['message'] else 400

    except Exception as e:
        return jsonify({"error":
                        f"Error updating university info: {str(e)}"}), 500


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
        return jsonify({"error":
                        f"Error deleting university info: {str(e)}"}), 500


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
        return jsonify({"error":
                        f"Error searching university info: {str(e)}"}), 500


@app.route('/api/university-info/categories', methods=['GET'])
def get_university_categories():
    """Get all unique categories"""
    try:
        result = university_service.get_categories()
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error":
                        f"Error retrieving categories: {str(e)}"}), 500


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
    app.run(host='0.0.0.0', port=5000, debug=True)
