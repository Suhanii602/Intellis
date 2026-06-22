from src.config import config

class AIProcessor:
    def __init__(self):
        self.provider = config.data['ai']['provider']
        self.api_keys = config.data['ai']['api_keys']
        self.client = None
        
        if self.provider == "gemini" and self.api_keys.get('gemini'):
            try:
                from google import genai
                self.client = genai.Client(api_key=self.api_keys['gemini'])
                print("✅ Gemini AI initialized!")
            except Exception as e:
                print(f"❌ Gemini init failed: {e}")
                self.provider = "local"
    
    def process(self, text):
        """Process text with AI"""
        if self.provider == "gemini" and self.client:
            return self._process_gemini(text)
        else:
            return self._process_local(text)
    
    def _process_gemini(self, text):
        """Process with Google Gemini using Markdown formatting"""
        try:
            # Enhanced prompt to request Markdown formatting
            prompt = f"""You are a helpful meeting assistant. Answer the following question using Markdown formatting for clarity.

Use:
- **bold** for key terms
- *italic* for emphasis  
- ## for main headings
- ### for subheadings
- `code` for technical terms
- - for bullet points
- 1. for numbered lists
- > for important notes
- Use tables for comparisons when helpful

Be concise, accurate, and well-structured.

Question: {text}

Answer (using Markdown):"""

            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )
            return response.text.strip()
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg:
                return "⚠️ API quota exceeded. Please wait a few minutes or switch to a new API key.\n\n💡 Tip: You can also use local mode by changing `\"provider\": \"local\"` in config.json."
            elif "404" in error_msg:
                return "⚠️ Model not found. Please check the model name in ai_processor.py."
            elif "503" in error_msg:
                return "⚠️ Gemini service is currently overloaded. Please try again in a few minutes."
            else:
                return f"❌ Gemini error: {error_msg[:200]}"
    
    def _process_local(self, text):
        """Fallback local responses"""
        text_lower = text.lower()
        
        if "what" in text_lower or "explain" in text_lower:
            return f"💡 **Local Mode:**\n\n*You asked: \"{text}\"*\n\nThis is a fallback response because the Gemini API is not available.\n\nTo enable real AI responses:\n1. Add a valid Gemini API key to `config.json`\n2. Set `\"provider\": \"gemini\"`\n3. Restart the app"
        elif "code" in text_lower or "python" in text_lower:
            return "💡 **Local Mode:**\n\n```python\n# This is a fallback response\n# For real AI coding assistance, enable Gemini API\nprint('Hello, World!')\n```"
        else:
            return f"💡 **Local Mode:**\n\n*You asked: \"{text}\"*\n\nPlease enable Gemini API for real AI responses."