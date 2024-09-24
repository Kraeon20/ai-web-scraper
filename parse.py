import google.generativeai as genai
import os
from dotenv import load_dotenv

template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)

load_dotenv()
GEMINI_KEY = os.environ.get('GEMINI_KEY')

genai.configure(api_key=GEMINI_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

def parse_with_gemini(dom_chunks, parse_description):
    parsed_results = []
    
    for i, chunk in enumerate(dom_chunks, start=1):
        prompt = template.format(dom_content=chunk, parse_description=parse_description)
        
        try:
            response = model.generate_content(prompt)
            
            if response.candidates and len(response.candidates) > 0:
                extracted_data = ''.join(part.text for part in response.candidates[0].content.parts).strip()
            else:
                extracted_data = ""
                
            print(f"Parsed batch: {i} of {len(dom_chunks)}")
            parsed_results.append(extracted_data)
        
        except Exception as e:
            print(f"Error while parsing batch {i}: {e}")
            parsed_results.append("")
    
    return "\n".join(parsed_results)