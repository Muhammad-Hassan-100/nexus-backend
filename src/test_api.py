"""
Test script for University Info API
Run this after starting the Flask server to test all endpoints
"""
import requests
import json

BASE_URL = "http://localhost:5000"

def test_health_check():
    """Test the health check endpoint"""
    print("Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        print("✅ Health check passed\n")
    except Exception as e:
        print(f"❌ Health check failed: {e}\n")

def test_create_info():
    """Test creating university info"""
    print("Testing create university info...")
    data = {
        "category": "test_category",
        "info": "This is test information for the university"
    }
    try:
        response = requests.post(f"{BASE_URL}/api/university-info", json=data)
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Response: {result}")
        if result.get('success'):
            print("✅ Create info passed")
            return result['data']['id']  # Return ID for further tests
        else:
            print("❌ Create info failed")
            return None
    except Exception as e:
        print(f"❌ Create info failed: {e}")
        return None
    print()

def test_get_all_info():
    """Test getting all university info"""
    print("Testing get all university info...")
    try:
        response = requests.get(f"{BASE_URL}/api/university-info")
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Response: {result}")
        if result.get('success'):
            print("✅ Get all info passed")
        else:
            print("❌ Get all info failed")
    except Exception as e:
        print(f"❌ Get all info failed: {e}")
    print()

def test_get_info_by_id(info_id):
    """Test getting university info by ID"""
    if not info_id:
        print("Skipping get by ID test (no ID available)\n")
        return
    
    print(f"Testing get university info by ID {info_id}...")
    try:
        response = requests.get(f"{BASE_URL}/api/university-info/{info_id}")
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Response: {result}")
        if result.get('success'):
            print("✅ Get info by ID passed")
        else:
            print("❌ Get info by ID failed")
    except Exception as e:
        print(f"❌ Get info by ID failed: {e}")
    print()

def test_update_info(info_id):
    """Test updating university info"""
    if not info_id:
        print("Skipping update test (no ID available)\n")
        return
    
    print(f"Testing update university info ID {info_id}...")
    data = {
        "category": "updated_test_category",
        "info": "This is updated test information"
    }
    try:
        response = requests.put(f"{BASE_URL}/api/university-info/{info_id}", json=data)
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Response: {result}")
        if result.get('success'):
            print("✅ Update info passed")
        else:
            print("❌ Update info failed")
    except Exception as e:
        print(f"❌ Update info failed: {e}")
    print()

def test_search_info():
    """Test searching university info"""
    print("Testing search university info...")
    try:
        response = requests.get(f"{BASE_URL}/api/university-info/search?q=test")
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Response: {result}")
        if result.get('success'):
            print("✅ Search info passed")
        else:
            print("❌ Search info failed")
    except Exception as e:
        print(f"❌ Search info failed: {e}")
    print()

def test_get_categories():
    """Test getting categories"""
    print("Testing get categories...")
    try:
        response = requests.get(f"{BASE_URL}/api/university-info/categories")
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Response: {result}")
        if result.get('success'):
            print("✅ Get categories passed")
        else:
            print("❌ Get categories failed")
    except Exception as e:
        print(f"❌ Get categories failed: {e}")
    print()

def test_delete_info(info_id):
    """Test deleting university info"""
    if not info_id:
        print("Skipping delete test (no ID available)\n")
        return
    
    print(f"Testing delete university info ID {info_id}...")
    try:
        response = requests.delete(f"{BASE_URL}/api/university-info/{info_id}")
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Response: {result}")
        if result.get('success'):
            print("✅ Delete info passed")
        else:
            print("❌ Delete info failed")
    except Exception as e:
        print(f"❌ Delete info failed: {e}")
    print()

def test_chat():
    """Test chat endpoint"""
    print("Testing chat endpoint...")
    data = {
        "message": "Tell me about DUET"
    }
    try:
        response = requests.post(f"{BASE_URL}/chat", json=data)
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Response: {result}")
        if 'response' in result:
            print("✅ Chat test passed")
        else:
            print("❌ Chat test failed")
    except Exception as e:
        print(f"❌ Chat test failed: {e}")
    print()

if __name__ == "__main__":
    print("🚀 Starting University Info API Tests\n")
    print("Make sure the Flask server is running on http://localhost:5000\n")
    
    # Run all tests
    test_health_check()
    created_id = test_create_info()
    test_get_all_info()
    test_get_info_by_id(created_id)
    test_update_info(created_id)
    test_search_info()
    test_get_categories()
    test_chat()
    test_delete_info(created_id)  # Clean up at the end
    
    print("🏁 All tests completed!")
