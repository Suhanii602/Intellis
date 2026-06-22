import json
import os
from pathlib import Path

class Config:
    def __init__(self):
        # Get the directory where this file is located
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.config_path = os.path.join(base_dir, "config.json")
        self.load_config()
        
    def load_config(self):
        with open(self.config_path, 'r') as f:
            self.data = json.load(f)
    
    @property
    def app_name(self):
        return self.data['app']['name']
    
    @property
    def window_size(self):
        return (self.data['app']['window']['width'], 
                self.data['app']['window']['height'])
    
    @property
    def hotkeys(self):
        return self.data['hotkeys']
    
    @property
    def colors(self):
        return self.data['colors']
    
    @property
    def tesseract_path(self):
        return self.data['paths']['tesseract']

config = Config()