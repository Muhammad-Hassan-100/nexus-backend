# University Bot API Documentation

## Overview
This API provides endpoints for managing university information and chat functionality. It uses Supabase as the database backend and includes full CRUD operations for university information.

## Base URL
```
http://localhost:5000
```

## Endpoints

### Chat API

#### POST /chat
Send a message to the university chat bot.

**Request Body:**
```json
{
  "message": "Tell me about DUET admission requirements"
}
```

**Response:**
```json
{
  "response": "For undergraduate admissions, applicants must have a minimum of 60% marks in HSC..."
}
```

### University Information API

#### 1. Create University Information
**POST** `/api/university-info`

**Request Body:**
```json
{
  "category": "admission_criteria",
  "info": "For undergraduate admissions, applicants must have a minimum of 60% marks in HSC and pass the DUET Entry Test."
}
```

**Response:**
```json
{
  "success": true,
  "message": "University info created successfully",
  "data": {
    "id": 1,
    "category": "admission_criteria",
    "info": "For undergraduate admissions...",
    "created_at": "2025-05-28T10:00:00Z",
    "updated_at": "2025-05-28T10:00:00Z"
  }
}
```

#### 2. Get All University Information
**GET** `/api/university-info`

**Response:**
```json
{
  "success": true,
  "message": "University info retrieved successfully",
  "data": [
    {
      "id": 1,
      "category": "admission_criteria",
      "info": "For undergraduate admissions...",
      "created_at": "2025-05-28T10:00:00Z",
      "updated_at": "2025-05-28T10:00:00Z"
    }
  ]
}
```

#### 3. Get University Information by ID
**GET** `/api/university-info/{id}`

**Response:**
```json
{
  "success": true,
  "message": "University info retrieved successfully",
  "data": {
    "id": 1,
    "category": "admission_criteria",
    "info": "For undergraduate admissions...",
    "created_at": "2025-05-28T10:00:00Z",
    "updated_at": "2025-05-28T10:00:00Z"
  }
}
```

#### 4. Get University Information by Category
**GET** `/api/university-info/category/{category}`

**Example:** `/api/university-info/category/admission_criteria`

**Response:**
```json
{
  "success": true,
  "message": "University info retrieved successfully",
  "data": [
    {
      "id": 1,
      "category": "admission_criteria",
      "info": "For undergraduate admissions...",
      "created_at": "2025-05-28T10:00:00Z",
      "updated_at": "2025-05-28T10:00:00Z"
    }
  ]
}
```

#### 5. Update University Information
**PUT** `/api/university-info/{id}`

**Request Body (partial update allowed):**
```json
{
  "category": "updated_admission_criteria",
  "info": "Updated information about admission requirements"
}
```

**Response:**
```json
{
  "success": true,
  "message": "University info updated successfully",
  "data": {
    "id": 1,
    "category": "updated_admission_criteria",
    "info": "Updated information...",
    "created_at": "2025-05-28T10:00:00Z",
    "updated_at": "2025-05-28T11:00:00Z"
  }
}
```

#### 6. Delete University Information
**DELETE** `/api/university-info/{id}`

**Response:**
```json
{
  "success": true,
  "message": "University info deleted successfully",
  "data": {
    "id": 1,
    "category": "admission_criteria",
    "info": "For undergraduate admissions...",
    "created_at": "2025-05-28T10:00:00Z",
    "updated_at": "2025-05-28T10:00:00Z"
  }
}
```

#### 7. Search University Information
**GET** `/api/university-info/search?q={query}`

**Example:** `/api/university-info/search?q=admission`

**Response:**
```json
{
  "success": true,
  "message": "Search completed successfully",
  "data": [
    {
      "id": 1,
      "category": "admission_criteria",
      "info": "For undergraduate admissions...",
      "created_at": "2025-05-28T10:00:00Z",
      "updated_at": "2025-05-28T10:00:00Z"
    }
  ]
}
```

#### 8. Get All Categories
**GET** `/api/university-info/categories`

**Response:**
```json
{
  "success": true,
  "message": "Categories retrieved successfully",
  "data": [
    "admission_criteria",
    "campus",
    "history",
    "overview",
    "postgraduate_programs",
    "undergraduate_programs"
  ]
}
```

#### 9. Health Check
**GET** `/api/health`

**Response:**
```json
{
  "status": "healthy",
  "message": "University Bot API is running",
  "endpoints": {
    "chat": "/chat",
    "university_info": "/api/university-info",
    "search": "/api/university-info/search",
    "categories": "/api/university-info/categories"
  }
}
```

## Error Responses

All endpoints return appropriate HTTP status codes and error messages:

**400 Bad Request:**
```json
{
  "error": "Category and info are required"
}
```

**404 Not Found:**
```json
{
  "success": false,
  "message": "University info not found",
  "data": null
}
```

**500 Internal Server Error:**
```json
{
  "error": "Error creating university info: [error details]"
}
```

## Database Schema

The `university_info` table has the following structure:
- `id`: Primary key (auto-increment)
- `category`: Category of the information (string)
- `info`: The actual information content (text)
- `created_at`: Timestamp when the record was created
- `updated_at`: Timestamp when the record was last updated

## Common Categories

Suggested categories for university information:
- `overview`: General information about the university
- `history`: Historical background
- `campus`: Campus facilities and locations
- `undergraduate_programs`: Bachelor's degree programs
- `postgraduate_programs`: Master's and PhD programs
- `admission_criteria`: Admission requirements
- `fees`: Fee structure
- `scholarships`: Available scholarships
- `faculty`: Faculty information
- `facilities`: University facilities
- `contact`: Contact information
- `events`: University events and activities

## Usage Examples

### Adding New Information
```bash
curl -X POST http://localhost:5000/api/university-info \
  -H "Content-Type: application/json" \
  -d '{"category": "fees", "info": "The fee structure for undergraduate programs is..."}'
```

### Searching Information
```bash
curl "http://localhost:5000/api/university-info/search?q=engineering"
```

### Getting by Category
```bash
curl "http://localhost:5000/api/university-info/category/admission_criteria"
```
