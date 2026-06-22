import pyautogui
import pyperclip
import time
import keyboard
from PIL import Image
import pytesseract
from src.config import config
import os

class TextSelector:
    def __init__(self):
        # Set tesseract path from config
        tesseract_path = config.tesseract_path
        if os.path.exists(tesseract_path):
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
        
    def get_selected_text(self):
        """Capture selected text using multiple methods"""
        
        # Method 1: Try clipboard (fastest)
        try:
            # Store original clipboard
            original = pyperclip.paste()
            
            # Copy selected text
            pyautogui.hotkey('ctrl', 'c')
            time.sleep(0.2)  # Wait for clipboard
            
            selected = pyperclip.paste()
            
            # Restore original if nothing new was copied
            if selected and selected != original:
                return selected.strip()
            
            # Restore original clipboard
            pyperclip.copy(original)
            
        except Exception as e:
            print(f"Clipboard method failed: {e}")
        
        # Method 2: OCR fallback
        return self.capture_screen_region()
    
    def capture_screen_region(self):
        """Use OCR to read text from screen region"""
        try:
            # Capture region around mouse (you can adjust this)
            x, y = pyautogui.position()
            region = (x-200, y-50, 400, 100)  # Width 400, height 100 around mouse
            
            screenshot = pyautogui.screenshot(region=region)
            text = pytesseract.image_to_string(screenshot)
            return text.strip()
        except Exception as e:
            print(f"OCR failed: {e}")
            return None
    
    def get_selected_text_enhanced(self):
        """Enhanced version with multiple attempts"""
        text = self.get_selected_text()
        
        if not text:
            # Try once more with longer delay
            time.sleep(0.5)
            text = self.get_selected_text()
            
        return text