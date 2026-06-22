# run_intellisai.py
import sys
import os

if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, base_path)
sys.path.insert(0, os.path.join(base_path, 'src'))

from src.overlay import ProfessionalOverlay
from src.ai_processor import AIProcessor
from src.config import config

class MeetingAssistant:
    def __init__(self):
        print("🚀 Starting Intellis AI...")
        self.overlay = ProfessionalOverlay()
        self.ai = AIProcessor()
        self.overlay.app = self
        print("✅ Ready!")
        
    def start(self):
        self.overlay.run()

if __name__ == "__main__":
    app = MeetingAssistant()
    app.start()