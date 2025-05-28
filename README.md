# University Bot Backend API

A comprehensive Flask-based REST API for managing university information with chat functionality, built with Supabase integration.

## Features

- 🤖 **Chat API**: Intelligent chatbot for university queries
- 📚 **University Info CRUD**: Complete Create, Read, Update, Delete operations
- 🔍 **Search Functionality**: Search through university information
- 📊 **Category Management**: Organize information by categories
- 🏥 **Health Check**: API health monitoring
- 🔐 **Supabase Integration**: Cloud database with real-time capabilities

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: Supabase (PostgreSQL)
- **AI/Chat**: LangChain with OpenAI/OpenRouter
- **Environment**: python-dotenv for configuration

## Project Structure

```
backend/
├── app.py                      # Main Flask application
├── chatllm.py                  # Chat functionality with LangChain
├── database.py                 # Supabase client configuration
├── university_service.py       # University info service layer
├── migrate_data.py            # Data migration script
├── test_api.py                # API testing script
├── university_info_table.sql  # SQL table creation commands
├── API_DOCUMENTATION.md       # Comprehensive API docs
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables
├── university_info.txt        # University information data
├── do_instructions.txt        # Chat instructions
├── dont_instructions.txt      # Chat restrictions
└── README.md                  # This file
```

## Setup and Installation

### 1. Clone and Navigate
```bash
cd "c:\Users\Muhammad Hassan\Desktop\University Bot\backend"
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration
The `.env` file is already configured with your Supabase credentials:
```env
SUPABASE_URL=https://gmibibayevqasoxcqmec.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### 4. Database Setup
1. In your Supabase dashboard, create the university_info table:
```sql
-- Copy and run the SQL commands from university_info_table.sql
```

2. Or run the SQL file directly in Supabase SQL Editor.

### 5. Populate Initial Data (Optional)
```bash
python migrate_data.py
```

### 6. Start the Server
```bash
python app.py
```

The API will be available at: `http://localhost:5000`

## API Endpoints

### Chat API
- `POST /chat` - Send message to chatbot

### University Info API
- `POST /api/university-info` - Create new information
- `GET /api/university-info` - Get all information
- `GET /api/university-info/{id}` - Get by ID
- `GET /api/university-info/category/{category}` - Get by category
- `PUT /api/university-info/{id}` - Update information
- `DELETE /api/university-info/{id}` - Delete information
- `GET /api/university-info/search?q={query}` - Search information
- `GET /api/university-info/categories` - Get all categories

### Utility
- `GET /api/health` - Health check

## Testing

Run the comprehensive test suite:
```bash
python test_api.py
```

This will test all endpoints and provide detailed feedback.

## Usage Examples

### Create University Information
```bash
curl -X POST http://localhost:5000/api/university-info `
  -H "Content-Type: application/json" `
  -d '{"category": "fees", "info": "Fee structure information here..."}'
```

### Search Information
```bash
curl "http://localhost:5000/api/university-info/search?q=engineering"
```

### Chat with Bot
```bash
curl -X POST http://localhost:5000/chat `
  -H "Content-Type: application/json" `
  -d '{"message": "Tell me about DUET admission requirements"}'
```

## Database Schema

The `university_info` table structure:
```sql
CREATE TABLE university_info (
    id SERIAL PRIMARY KEY,
    category VARCHAR(255) NOT NULL,
    info TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

## Common Categories

- `overview` - General university information
- `history` - Historical background
- `campus` - Campus facilities and locations
- `undergraduate_programs` - Bachelor's programs
- `postgraduate_programs` - Master's and PhD programs
- `admission_criteria` - Admission requirements
- `fees` - Fee structure
- `scholarships` - Available scholarships
- `contact` - Contact information

## Error Handling

The API provides comprehensive error handling with appropriate HTTP status codes:
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `404` - Not Found
- `500` - Internal Server Error

## Development

### Adding New Features
1. Update `university_service.py` for new business logic
2. Add endpoints in `app.py`
3. Update `API_DOCUMENTATION.md`
4. Add tests in `test_api.py`

### Code Structure
- **Service Layer**: `university_service.py` handles all business logic
- **Database Layer**: `database.py` manages Supabase connection
- **API Layer**: `app.py` defines REST endpoints
- **Chat Layer**: `chatllm.py` handles AI chat functionality

## Deployment Considerations

- Ensure Supabase credentials are secure
- Use environment variables for production
- Consider rate limiting for production use
- Set up proper logging and monitoring
- Configure CORS for frontend domains

## Contributing

1. Follow the existing code structure
2. Add comprehensive error handling
3. Update documentation for new features
4. Add tests for new functionality
5. Keep the API clean and RESTful

## Support

For issues or questions:
1. Check the API documentation
2. Run the test suite to identify issues
3. Verify Supabase connection and table structure
4. Ensure all environment variables are set correctly
