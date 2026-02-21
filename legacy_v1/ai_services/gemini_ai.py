"""
Google Gemini AI Service - FREE & POWERFUL
60 requests per minute - No credit card needed!
"""

import google.generativeai as genai
import json
import os


class GeminiAI:
    """Google Gemini AI wrapper"""
    
    def __init__(self, api_key=None):
        """Initialize Gemini"""
        self.api_key = api_key or os.environ.get('GOOGLE_GEMINI_API_KEY')
        
        if not self.api_key:
            raise ValueError("⚠️ Google Gemini API key not found in .env file!")
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        
        # Use Gemini 1.5 Flash (fastest & free)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        print("✅ Google Gemini AI initialized!")
    
    def generate(self, prompt, temperature=0.7, max_tokens=2000):
        """
        Generate text response
        
        Args:
            prompt: Your prompt
            temperature: Creativity (0-1)
            max_tokens: Max response length
            
        Returns:
            Generated text
        """
        try:
            generation_config = {
                'temperature': temperature,
                'max_output_tokens': max_tokens,
            }
            
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            return response.text
            
        except Exception as e:
            print(f"❌ Gemini error: {e}")
            return None
    
    def generate_json(self, prompt, max_tokens=3000):
        """
        Generate JSON response (for structured data)
        
        Args:
            prompt: Your prompt (should ask for JSON)
            max_tokens: Max response length
            
        Returns:
            Parsed JSON dict
        """
        try:
            # Add strict JSON instruction
            full_prompt = f"""{prompt}

CRITICAL: Return ONLY valid JSON. No markdown, no explanations, no text before or after JSON.
Start directly with {{ and end with }}"""
            
            response_text = self.generate(full_prompt, temperature=0.3, max_tokens=max_tokens)
            
            if not response_text:
                return None
            
            # Clean response
            cleaned = response_text.strip()
            
            # Remove markdown code blocks if present
            if '```json' in cleaned:
                cleaned = cleaned.split('```json')[1].split('```')[0].strip()
            elif '```' in cleaned:
                cleaned = cleaned.split('```')[1].split('```')[0].strip()
            
            # Parse JSON
            result = json.loads(cleaned)
            
            return result
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON parse error: {e}")
            print(f"Raw response: {response_text[:300] if response_text else 'None'}")
            return None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def chat(self, messages):
        """
        Multi-turn conversation
        
        Args:
            messages: List of {'role': 'user/assistant', 'content': 'text'}
            
        Returns:
            Response text
        """
        try:
            # Start chat
            chat = self.model.start_chat(history=[])
            
            # Send messages
            for msg in messages:
                if msg['role'] == 'user':
                    response = chat.send_message(msg['content'])
            
            return response.text
            
        except Exception as e:
            print(f"❌ Chat error: {e}")
            return None


def create_gemini_ai(api_key=None):
    """Create Gemini AI instance"""
    return GeminiAI(api_key)


# Test function
if __name__ == "__main__":
    print("Testing Google Gemini AI...")
    try:
        gemini = create_gemini_ai()
        response = gemini.generate("Say 'Hello from Gemini!' in a creative way")
        print(f"Response: {response}")
    except Exception as e:
        print(f"Error: {e}")