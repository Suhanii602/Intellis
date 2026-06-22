import json
import os

print("🔍 DEBUG: Checking config.json")
print("="*50)

# Check if file exists
if os.path.exists("config.json"):
    print("✅ config.json found")
else:
    print("❌ config.json NOT found")
    exit()

# Load and check content
with open("config.json", "r") as f:
    config = json.load(f)

print("\n📋 Config content:")
print(f"  AI Provider: {config['ai']['provider']}")
print(f"  Gemini API Key present: {'Yes' if config['ai']['api_keys']['gemini'] else 'No'}")

if config['ai']['api_keys']['gemini']:
    key = config['ai']['api_keys']['gemini']
    print(f"  Key starts with: {key[:10]}... (length: {len(key)})")

print("\n" + "="*50)
print("Try importing AI Processor now...")

try:
    from src.ai_processor import AIProcessor
    ai = AIProcessor()
    print(f"✅ AI Processor initialized, provider: {ai.provider}")
except Exception as e:
    print(f"❌ Error: {e}")