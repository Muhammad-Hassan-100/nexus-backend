import sys
import os
sys.path.append('src')
from src.database import get_supabase_client

def read_instruction_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading instruction file {file_path}: {str(e)}")
        return ""

def get_university_info_from_database():
    """Fetch university information from database"""
    try:
        supabase = get_supabase_client()
        result = supabase.table("university_info").select("category, info").order("category").execute()
        
        if result.data:
            university_info = ""
            for item in result.data:
                university_info += f"\n{item['category'].upper().replace('_', ' ')}:\n{item['info']}\n"
            return university_info
        else:
            return "No university information available in database."
    except Exception as e:
        print(f"Error fetching university info from database: {str(e)}")
        return "Error loading university information from database."

current_dir = os.path.dirname(os.path.abspath(__file__))
do_instructions_path = os.path.join(current_dir, "src", "do_instructions.txt")
dont_instructions_path = os.path.join(current_dir, "src", "dont_instructions.txt")

do_instructions = read_instruction_file(do_instructions_path)
dont_instructions = read_instruction_file(dont_instructions_path)

# Get all the data being sent to API
university_info = get_university_info_from_database()

# Create a rough estimate of the system prompt
system_prompt = f"""You are a helpful assistant for Dawood University of Engineering & Technology (DUET). Answer questions about the university and other academic topics.

GREETING RULE: Only respond with greetings (like "Hello", "Hi", "Assalam o Alaikum", etc.) if the user has greeted you first with words like hello, hi, hey, assalam, salam, good morning, etc. Otherwise, directly answer their question without any greeting.

RESPONSE GUIDELINES:
- BE CONTEXTUALLY PRECISE: Analyze the exact question and provide the most relevant, specific answer  
- AVOID GENERIC RESPONSES: Different questions require different answers, even about the same topic
- BE DIRECT AND TO-THE-POINT: Give concise but complete answers (2-4 sentences)
- PROVIDE ADEQUATE INFORMATION: Include relevant details without being lengthy
- PROVIDE LOGICAL CALCULATIONS: 
  * For "When established?" questions → Give the year (1962)
  * For "How long established?" questions → Calculate duration (e.g., "63 years since 1962")
  * For duration questions, always calculate from 1962 to current year (2025)

UNIVERSITY INFORMATION:
{university_info}

BEHAVIOR INSTRUCTIONS:
{do_instructions}

RESTRICTIONS:
{dont_instructions}"""

print('=== TOKEN ANALYSIS REPORT ===')
print()
print('INDIVIDUAL COMPONENT SIZES:')
print(f'University Info: {len(university_info):,} characters')
print(f'Do Instructions: {len(do_instructions):,} characters') 
print(f'Dont Instructions: {len(dont_instructions):,} characters')
print(f'Base Prompt: ~500 characters')
print()
print(f'TOTAL SYSTEM PROMPT: {len(system_prompt):,} characters')
print()

# Rough token estimation (1 token ≈ 4 characters for English text)
estimated_tokens = len(system_prompt) // 4
print('=== TOKEN ESTIMATION ===')
print(f'Estimated System Prompt Tokens: ~{estimated_tokens:,}')
print()

print('=== MODEL INFORMATION ===')
print('Current Model: google/gemini-2.0-flash-exp:free')
print('Model Context Length: 1,048,576 tokens (1M tokens)')
print('Recommended Max Input: 900,000 tokens (leaving space for response)')
print()

print('=== ANALYSIS RESULT ===')
if estimated_tokens > 900000:
    print('❌ WARNING: Current system prompt is TOO LARGE!')
    print(f'   Current: ~{estimated_tokens:,} tokens')
    print('   Recommended: <900,000 tokens')
    print('   Exceeds limit by: ~{:,} tokens'.format(estimated_tokens - 900000))
    print()
    print('RECOMMENDATIONS:')
    print('1. Shorten university information in database')
    print('2. Reduce instruction file lengths')
    print('3. Use a model with larger context window')
    
elif estimated_tokens > 50000:
    print('⚠️  CAUTION: System prompt is large but acceptable')
    print(f'   Current: ~{estimated_tokens:,} tokens')
    print('   Available for user input: ~{:,} tokens'.format(900000 - estimated_tokens))
    print('   Available for response: ~100,000 tokens')
    
else:
    print('✅ Current system prompt size is OPTIMAL')
    print(f'   Current: ~{estimated_tokens:,} tokens')
    print('   Available for user input: ~{:,} tokens'.format(900000 - estimated_tokens))
    print('   Available for response: ~100,000 tokens')

print()
print('=== SAMPLE SIZES FOR CONTEXT ===')
print('• Small message: ~25 tokens')
print('• Medium message: ~100 tokens') 
print('• Large message: ~300 tokens')
print('• Chat history (10 messages): ~500-1000 tokens')
