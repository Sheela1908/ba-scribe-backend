from google import genai
from google.genai import types
import base64
import io

# Your existing API Key
GEMINI_API_KEY = "AIzaSyDC4GUp6ad2s4V53IXRpuiXXtSiqAoGfKk"

def generate_ba_docs(input_data, mime_type="text/plain"):
    """
    Handles Text, Images, and Audio.
    mime_type can be: 'text/plain', 'image/png', 'image/jpeg', or 'audio/mpeg'
    """
    client = genai.Client(
        api_key=GEMINI_API_KEY,
        http_options=types.HttpOptions(
            retry_options=types.HttpRetryOptions(
                attempts=3,
                initial_delay=2.0,
                max_delay=10.0
            )
        )
    )

    # This is the 'Core Instruction' that stays the same regardless of input type
    base_prompt = """
    You are an expert HR-Tech Business Analyst. 
    Analyze the provided input (it could be text, an image of a whiteboard, or an audio recording) 
    and generate a professional BA document including:
    1. A User Story (As a... I want... So that...).
    2. Five clear Acceptance Criteria.
    3. A 'Gap Analysis' (3 missing details to ask stakeholders).
    4. MoSCoW Prioritization.
    """

    try:
        if mime_type == "text/plain":
            # CASE 1: Standard Text Input
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=f"{base_prompt}\n\nNotes to analyze: {input_data}"
            )
        else:
            # CASE 2: Image or Audio (Multimodal)
            # We decode the Base64 string sent from React back into bytes
            file_bytes = base64.b64decode(input_data)
            
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=[
                    base_prompt,
                    types.Part.from_bytes(data=file_bytes, mime_type=mime_type)
                ]
            )
        
        return response.text

    except Exception as e:
        return f"Error during AI analysis: {str(e)}"

# Quick test area
if __name__ == "__main__":
    # Test Text
    print("--- Testing Text ---")
    print(generate_ba_docs("Need a payroll system for remote employees."))