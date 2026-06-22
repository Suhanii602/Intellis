import sys
import os
if getattr(sys, 'frozen', False):
    os.chdir(os.path.dirname(sys.executable))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from overlay import ProfessionalOverlay
from ai_processor import AIProcessor
from config import config

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