import pyautogui
import time
from PIL import Image
import os
from datetime import datetime
from src.config import config

class ScreenCapture:
    def __init__(self):
        self.temp_folder = config.data['paths']['temp_folder']
        os.makedirs(self.temp_folder, exist_ok=True)
    
    def capture_region(self, region=None):
        """
        Capture a specific region of the screen
        
        Args:
            region: (x, y, width, height) tuple. If None, captures around mouse
        
        Returns:
            PIL Image object
        """
        if region is None:
            # Capture region around mouse (400x400 area)
            x, y = pyautogui.position()
            region = (x-200, y-200, 400, 400)
        
        screenshot = pyautogui.screenshot(region=region)
        return screenshot
    
    def capture_full_screen(self):
        """Capture entire screen"""
        return pyautogui.screenshot()
    
    def save_temp_image(self, image):
        """Save image to temp folder and return path"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"capture_{timestamp}.png"
        filepath = os.path.join(self.temp_folder, filename)
        image.save(filepath)
        return filepath
    
    def capture_and_get_path(self, region=None):
        """Capture and save image, return path"""
        img = self.capture_region(region)
        return self.save_temp_image(img)