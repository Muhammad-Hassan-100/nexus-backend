import os
import psycopg2
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = "https://gmibibayevqasoxcqmec.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdtaWJpYmF5ZXZxYXNveGNxbWVjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDg0MTAyMzksImV4cCI6MjA2Mzk4NjIzOX0.t3OL_4jNXzamqahehaMmS_rj60gvnPqnadXB7qrD45c"

DATABASE_URL = os.getenv(
    "DATABASE_URL"
) or "postgresql://postgres.gmibibayevqasoxcqmec:DuetUniversity2024@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def get_supabase_client():
    """Return the Supabase client instance"""
    return supabase


def get_connection():
    """Return a direct PostgreSQL connection for authentication operations"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        raise
