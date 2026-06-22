import sounddevice as sd
import numpy as np
import whisper
import queue
import threading
import time
import os
from src.config import config

class AudioProcessor:
    def __init__(self):
        self.audio_queue = queue.Queue()
        self.is_running = False
        self.message_callback = None
        self.question_callback = None
        self.sample_rate = config.data['audio']['sample_rate']
        
        # Load Whisper model (tiny for speed, base for accuracy)
        print("Loading Whisper model...")
        self.model = whisper.load_model("base.en")  # Use "base" for better accuracy
        print("Whisper model loaded!")
        
    def set_callbacks(self, message_callback=None, question_callback=None):
        self.message_callback = message_callback
        self.question_callback = question_callback
    
    def start(self):
        """Start audio capture and processing"""
        self.is_running = True
        
        # Find CABLE Input device
        devices = sd.query_devices()
        cable_device = None
        
        for i, device in enumerate(devices):
            if "CABLE Input" in device['name'] or "CABLE Output" in device['name']:
                cable_device = i
                break
        
        if cable_device is None:
            if self.message_callback:
                self.message_callback(
                    "⚠️ VB-CABLE not found. Install from vb-audio.com/Cable/",
                    "#ffaa00"
                )
            return
        
        # Start audio stream from CABLE device
        def audio_callback(indata, frames, time, status):
            if self.is_running:
                self.audio_queue.put(indata.copy())
        
        try:
            self.stream = sd.InputStream(
                device=cable_device,
                callback=audio_callback,
                channels=config.data['audio']['channels'],
                samplerate=self.sample_rate
            )
            self.stream.start()
            
            if self.message_callback:
                self.message_callback("🎤 Audio capture started", "#00ff88")
            
            # Start processing thread
            self.process_thread = threading.Thread(target=self.process_audio, daemon=True)
            self.process_thread.start()
            
        except Exception as e:
            if self.message_callback:
                self.message_callback(f"❌ Audio error: {str(e)}", "#ff4444")
    
    def process_audio(self):
        """Process audio chunks and detect questions"""
        audio_buffer = []
        buffer_duration = config.data['audio']['chunk_duration']
        buffer_size = int(self.sample_rate * buffer_duration)
        
        while self.is_running:
            try:
                # Collect audio
                while len(audio_buffer) < buffer_size:
                    if not self.audio_queue.empty():
                        audio_buffer.extend(self.audio_queue.get().flatten())
                    time.sleep(0.1)
                
                # Convert to numpy array
                audio_array = np.array(audio_buffer[:buffer_size], dtype=np.float32)
                
                # Transcribe
                result = self.model.transcribe(audio_array, language='en')
                text = result["text"].strip()
                
                if text and len(text) > 10:  # Ignore very short phrases
                    print(f"Transcribed: {text}")
                    
                    if self.is_question(text):
                        if self.question_callback:
                            self.question_callback(text)
                    
                    if self.message_callback:
                        self.message_callback(f"🎤 {text}", "#888888")
                
                audio_buffer = audio_buffer[buffer_size:]
                
            except Exception as e:
                print(f"Audio processing error: {e}")
                time.sleep(1)
    
    def is_question(self, text):
        """Detect if text is a question"""
        question_words = ['what', 'why', 'how', 'when', 'where', 'who',
                         'can you', 'could you', 'would you', 'is there',
                         'are there', 'do you', 'does anyone', 'anyone know']
        text_lower = text.lower()
        return any(q in text_lower for q in question_words) or '?' in text
    
    def stop(self):
        self.is_running = False
        if hasattr(self, 'stream'):
            self.stream.stop()