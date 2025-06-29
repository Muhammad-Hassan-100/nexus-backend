from flask import Flask, request, jsonify
from flask_cors import CORS
from src.chatllm import chat_response
from src.university_service import UniversityInfoService
import os
from src.database import get_supabase_client
from datetime import datetime
import uuid


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
    session_id = request.json.get('session_id', 'default')
    
    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    try:
        response = chat_response(user_input, session_id)
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


@app.route('/api/notifications', methods=['GET'])
def get_notifications():
    """Get all notifications"""
    try:
        is_active = request.args.get('active')
        notification_type = request.args.get('type')

        query = supabase.table('notifications').select('*')

        if is_active is not None:
            active_bool = is_active.lower() == 'true'
            query = query.eq('is_active', active_bool)

        if notification_type:
            query = query.eq('type', notification_type)

        result = query.order('created_at', desc=True).execute()

        return jsonify({"success": True, "notifications": result.data}), 200

    except Exception as e:
        print(f"Error fetching notifications: {e}")
        return jsonify({
            "success": False,
            "message": "Failed to fetch notifications"
        }), 500


@app.route('/api/notifications/active', methods=['GET'])
def get_active_notifications():
    """Get only active notifications"""
    try:
        result = supabase.table('notifications').select('*').eq(
            'is_active', True).order('created_at', desc=True).execute()

        return jsonify({
            "success": True,
            "notifications": result.data
        }), 200

    except Exception as e:
        print(f"Error fetching active notifications: {e}")
        return jsonify({
            "success": False,
            "message": "Failed to fetch active notifications"
        }), 500


@app.route('/api/notifications', methods=['POST'])
def create_notification():
    """Create a new notification"""
    try:
        data = request.get_json()
        print(f"DEBUG: Received notification data: {data}")

        required_fields = ['title', 'message', 'type']
        for field in required_fields:
            if field not in data:
                print(f"DEBUG: Missing required field: {field}")
                return jsonify({
                    "success": False,
                    "message": f"Missing required field: {field}"
                }), 400

        notification_data = {
            'title': data['title'],
            'message': data['message'],
            'type': data['type'],
            'start_date': '1900-01-01',  # Default old date
            'end_date': '2099-12-31',    # Default far future date
            'start_time': '00:00',       # Default start time
            'end_time': '23:59',         # Default end time
            'is_active': data.get('isActive', True),
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }

        print(f"DEBUG: Notification data to insert: {notification_data}")

        result = supabase.table('notifications').insert(
            notification_data).execute()

        print(f"DEBUG: Supabase result: {result}")

        return jsonify({
            "success": True,
            "message": "Notification created successfully",
            "notification": result.data[0] if result.data else None
        }), 201

    except Exception as e:
        print(f"Error creating notification: {e}")
        print(f"DEBUG: Exception type: {type(e)}")
        print(f"DEBUG: Exception args: {e.args}")
        return jsonify({
            "success": False,
            "message": "Failed to create notification"
        }), 500


@app.route('/api/notifications/<notification_id>', methods=['PUT'])
def update_notification(notification_id):
    """Update an existing notification"""
    try:
        data = request.get_json()

        update_data = {'updated_at': datetime.now().isoformat()}

        allowed_fields = ['title', 'message', 'type', 'isActive']
        field_mapping = {
            'isActive': 'is_active'
        }

        for field in allowed_fields:
            if field in data:
                db_field = field_mapping.get(field, field)
                update_data[db_field] = data[field]

        result = supabase.table('notifications').update(update_data).eq(
            'id', notification_id).execute()

        if not result.data:
            return jsonify({
                "success": False,
                "message": "Notification not found"
            }), 404

        return jsonify({
            "success": True,
            "message": "Notification updated successfully",
            "notification": result.data[0]
        }), 200

    except Exception as e:
        print(f"Error updating notification: {e}")
        return jsonify({
            "success": False,
            "message": "Failed to update notification"
        }), 500


@app.route('/api/notifications/<notification_id>', methods=['DELETE'])
def delete_notification(notification_id):
    """Delete a notification"""
    try:
        result = supabase.table('notifications').delete().eq(
            'id', notification_id).execute()

        if not result.data:
            return jsonify({
                "success": False,
                "message": "Notification not found"
            }), 404

        return jsonify({
            "success": True,
            "message": "Notification deleted successfully"
        }), 200

    except Exception as e:
        print(f"Error deleting notification: {e}")
        return jsonify({
            "success": False,
            "message": "Failed to delete notification"
        }), 500


@app.route('/api/notifications/<notification_id>/toggle', methods=['PATCH'])
def toggle_notification_status(notification_id):
    """Toggle notification active status"""
    try:
        data = request.get_json()
        print(f"Toggle request data: {data}")

        if not data:
            return jsonify({
                "success": False,
                "message": "Request body is required"
            }), 400

        is_active = data.get('isActive', True)
        print(
            f"Toggling notification {notification_id} to active: {is_active}")

        result = supabase.table('notifications').update({
            'is_active':
            is_active,
            'updated_at':
            datetime.now().isoformat()
        }).eq('id', notification_id).execute()

        if not result.data:
            return jsonify({
                "success": False,
                "message": "Notification not found"
            }), 404

        return jsonify({
            "success": True,
            "message":
            f"Notification {'activated' if is_active else 'deactivated'} successfully",
            "notification": result.data[0]
        }), 200

    except Exception as e:
        print(f"Error toggling notification status: {e}")
        return jsonify({
            "success":
            False,
            "message":
            f"Failed to toggle notification status: {str(e)}"
        }), 500


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
            "categories": "/api/university-info/categories",
            "notifications": "/api/notifications",
            "active_notifications": "/api/notifications/active"
        }
    }), 200


@app.route('/')
def home():
    return "I'm alive!"

@app.route('/test-api')
def test_api():
    return jsonify({"message": "Test API route working", "success": True})

@app.route('/api/auth/get-api-key', methods=['GET'])
def get_api_key_route():
    """Get current API key from database"""
    try:
        result = supabase.table('api_settings').select('api_key').limit(1).execute()

        if result.data and len(result.data) > 0:
            api_key = result.data[0]['api_key']
            masked_key = api_key[:8] + '*' * (len(api_key) - 12) + api_key[-4:]
            return jsonify({
                "success": True,
                "message": "API key retrieved successfully",
                "api_key": masked_key,
                "full_key": api_key
            }), 200
        else:
            return jsonify({
                "success": False,
                "message": "No API key found in database"
            }), 404

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Get API key error: {str(e)}"
        }), 500

@app.route('/api/auth/update-api-key', methods=['PUT'])
def update_api_key_route():
    """Update API key in database"""
    try:
        data = request.get_json()

        if not data or 'api_key' not in data:
            return jsonify({
                "success": False,
                "message": "API key is required"
            }), 400

        api_key = data['api_key'].strip()

        if not api_key:
            return jsonify({
                "success": False,
                "message": "API key cannot be empty"
            }), 400

        check_result = supabase.table('api_settings').select('id').limit(1).execute()

        if check_result.data and len(check_result.data) > 0:
            result = supabase.table('api_settings').update({
                'api_key': api_key,
                'updated_at': datetime.now().isoformat()
            }).eq('id', check_result.data[0]['id']).execute()
        else:
            result = supabase.table('api_settings').insert({
                'api_key': api_key,
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }).execute()

        if result.data:
            return jsonify({
                "success": True,
                "message": "API key updated successfully"
            }), 200
        else:
            return jsonify({
                "success": False,
                "message": "Failed to update API key"
            }), 500

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Update API key error: {str(e)}"
        }), 500

if __name__ == '__main__':
    app.run()
