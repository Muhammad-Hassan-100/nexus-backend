import psycopg2
import sys
from datetime import datetime

def connect_to_database():
    """Connect to PostgreSQL database"""
    try:
        connection = psycopg2.connect(
            host="localhost",
            port="5432",
            database="chatbot",
            user="postgres",
            password="54321"
        )
        return connection
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

def get_all_tables(cursor):
    """Get all table names from the database"""
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_type = 'BASE TABLE'
        ORDER BY table_name;
    """)
    return [table[0] for table in cursor.fetchall()]

def get_table_columns(cursor, table_name):
    """Get column information for a specific table"""
    cursor.execute("""
        SELECT column_name, data_type, is_nullable, column_default
        FROM information_schema.columns 
        WHERE table_schema = 'public' 
        AND table_name = %s
        ORDER BY ordinal_position;
    """, (table_name,))
    return cursor.fetchall()

def get_table_data(cursor, table_name):
    """Get all data from a specific table"""
    try:
        cursor.execute(f'SELECT * FROM "{table_name}"')
        return cursor.fetchall()
    except Exception as e:
        return f"Error fetching data: {e}"

def extract_database_info():
    """Main function to extract all database information"""
    connection = connect_to_database()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        output = []
        output.append("=" * 80)
        output.append(f"DATABASE EXPORT - PostgreSQL Database: chatbot")
        output.append(f"Export Date: {timestamp}")
        output.append("=" * 80)
        output.append("")
        
        tables = get_all_tables(cursor)
        output.append(f"TOTAL TABLES FOUND: {len(tables)}")
        output.append("-" * 50)
        
        for table_name in tables:
            output.append(f"\nTABLE: {table_name}")
            output.append("=" * (len(table_name) + 7))
            
            columns = get_table_columns(cursor, table_name)
            output.append("\nCOLUMN STRUCTURE:")
            output.append("-" * 20)
            for col in columns:
                col_name, data_type, is_nullable, default_val = col
                nullable = "NULL" if is_nullable == "YES" else "NOT NULL"
                default = f" DEFAULT: {default_val}" if default_val else ""
                output.append(f"  {col_name} | {data_type} | {nullable}{default}")
            
            output.append(f"\nDATA FROM {table_name}:")
            output.append("-" * (len(table_name) + 11))
            
            data = get_table_data(cursor, table_name)
            if isinstance(data, str):
                output.append(f"  {data}")
            elif not data:
                output.append("  (No data found)")
            else:
                col_names = [col[0] for col in columns]
                output.append(f"  {' | '.join(col_names)}")
                output.append(f"  {'-' * (len(' | '.join(col_names)))}")
                
                for row in data:
                    formatted_row = []
                    for item in row:
                        if item is None:
                            formatted_row.append('NULL')
                        else:
                            str_item = str(item).replace('\n', '\\n').replace('\r', '\\r')
                            formatted_row.append(str_item)
                    output.append(f"  {' | '.join(formatted_row)}")
            
            output.append("\n" + "=" * 80)
        
        output_file = "database_export.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(output))
        
        print(f"Database export completed successfully!")
        print(f"Output saved to: {output_file}")
        print(f"Total tables exported: {len(tables)}")
        
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"Error during extraction: {e}")
        if connection:
            connection.close()
        return False

if __name__ == "__main__":
    success = extract_database_info()
    if not success:
        sys.exit(1)
