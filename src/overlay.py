import customtkinter as ctk
import win32gui
import win32con
import ctypes
from datetime import datetime
from src.config import config
import threading
import time

# Set appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class ProfessionalOverlay:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title(config.app_name)
        self.setup_window()
        self.setup_ui()
        self.app = None
        self.is_stealth = False
        self.is_listening = False
        
    def setup_window(self):
        width = 550
        height = 680
        screen_width = self.root.winfo_screenwidth()
        x = screen_width - width - 20
        y = 40
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
        self.root.attributes('-topmost', True)
        self.root.overrideredirect(True)
        self.root.attributes('-alpha', 0.88)
        self.root.configure(fg_color="#0d1117")
        
        self.root.bind('<Button-1>', self.start_move)
        self.root.bind('<B1-Motion>', self.on_move)
        
        self.root.bind('<Map>', self._on_map)
        self.root.after(100, self.apply_display_affinity)
    
    def _on_map(self, event):
        self.root.overrideredirect(True)
        self.root.lift()
        self.root.focus_force()
    
    def apply_display_affinity(self):
        try:
            self.root.update()
            hwnd = win32gui.FindWindow(None, config.app_name)
            if hwnd:
                WDA_EXCLUDEFROMCAPTURE = 0x00000011
                user32 = ctypes.WinDLL('user32', use_last_error=True)
                user32.SetWindowDisplayAffinity(hwnd, WDA_EXCLUDEFROMCAPTURE)
        except Exception as e:
            print(f"Display affinity error: {e}")
    
    def start_move(self, event):
        self.x = event.x
        self.y = event.y
    
    def on_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")
    
    def minimize(self):
        try:
            self.root.overrideredirect(False)
            self.root.iconify()
            self.root.after(200, lambda: self.root.overrideredirect(True))
        except Exception as e:
            print(f"Minimize error: {e}")
    
    def setup_ui(self):
        """Glassmorphism UI with clear Q&A distinction using CTkTextbox"""
        
        self.main_frame = ctk.CTkFrame(
            self.root, 
            fg_color="#0d1117", 
            corner_radius=16,
            border_width=1,
            border_color="#2d3748"
        )
        self.main_frame.pack(fill='both', expand=True, padx=2, pady=2)
        
        # ===== TOP BAR =====
        self.top_bar = ctk.CTkFrame(
            self.main_frame, 
            height=50, 
            fg_color="#161b22",
            corner_radius=12
        )
        self.top_bar.pack(fill='x', padx=8, pady=(8, 4))
        self.top_bar.pack_propagate(False)
        
        self.top_bar.bind('<Button-1>', self.start_move)
        self.top_bar.bind('<B1-Motion>', self.on_move)
        
        title_label = ctk.CTkLabel(
            self.top_bar, 
            text="✨ INTELLIS AI",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#00ff88"
        )
        title_label.pack(side='left', padx=15, pady=12)
        title_label.bind('<Button-1>', self.start_move)
        title_label.bind('<B1-Motion>', self.on_move)
        
        self.status_dot = ctk.CTkLabel(
            self.top_bar,
            text="● ACTIVE",
            font=ctk.CTkFont(size=11),
            text_color="#00ff88"
        )
        self.status_dot.pack(side='left', padx=10)
        
        self.timer_label = ctk.CTkLabel(
            self.top_bar,
            text="00:00",
            font=ctk.CTkFont(size=10),
            text_color="#666666"
        )
        self.timer_label.pack(side='left', padx=12)
        
        btn_frame = ctk.CTkFrame(self.top_bar, fg_color="transparent")
        btn_frame.pack(side='right', padx=10)
        
        self.stealth_btn = ctk.CTkButton(
            btn_frame, 
            text="👻", 
            width=32, 
            height=32, 
            fg_color="transparent",
            hover_color="#2d2d2d",
            font=ctk.CTkFont(size=14),
            command=self.toggle_stealth
        )
        self.stealth_btn.pack(side='left', padx=2)
        
        min_btn = ctk.CTkButton(
            btn_frame, 
            text="─", 
            width=32, 
            height=32, 
            fg_color="transparent",
            hover_color="#2d2d2d",
            font=ctk.CTkFont(size=14),
            command=self.minimize
        )
        min_btn.pack(side='left', padx=2)
        
        close_btn = ctk.CTkButton(
            btn_frame, 
            text="✕", 
            width=32, 
            height=32, 
            fg_color="transparent",
            hover_color="#ff4444",
            font=ctk.CTkFont(size=12),
            command=self.quit
        )
        close_btn.pack(side='left', padx=2)
        
        # ===== ACTION BAR =====
        self.action_bar = ctk.CTkFrame(
            self.main_frame,
            height=45,
            fg_color="#161b22",
            corner_radius=12
        )
        self.action_bar.pack(fill='x', padx=8, pady=4)
        self.action_bar.pack_propagate(False)
        
        actions = [
            ("🎤 Listen", self.toggle_listening),
            ("📸 Full", self.capture_full_screen),
            ("📐 Region", self.capture_region),
            ("📋 Copy", self.copy_last_answer),
            ("🧹 Clear", self.clear_messages)
        ]
        
        for text, command in actions:
            btn = ctk.CTkButton(
                self.action_bar,
                text=text,
                height=34,
                corner_radius=8,
                fg_color="#1a1a2e",
                hover_color="#2a2a3e",
                font=ctk.CTkFont(size=11),
                command=command
            )
            btn.pack(side='left', padx=4, pady=5)
        
        # ===== CHAT DISPLAY (CTkTextbox - RELIABLE) =====
        self.chat_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="#0d1117",
            corner_radius=12,
            border_width=1,
            border_color="#2d3748"
        )
        self.chat_frame.pack(fill='both', expand=True, padx=10, pady=(4, 8))
        
        self.chat_display = ctk.CTkTextbox(
            self.chat_frame,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            fg_color="#0d1117",
            text_color="#e6edf3",
            wrap='word',
            border_width=0,
            corner_radius=10
        )
        self.chat_display.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Configure tags for Q&A distinction
        # USER (GREEN)
        self.chat_display._textbox.tag_config("user_label",
            foreground="#00ff88",
            font=("Segoe UI", 10, "bold"),
            spacing3=5
        )
        self.chat_display._textbox.tag_config("user_bubble",
            background="#1a3a2a",
            foreground="#00ff88",
            font=("Segoe UI", 12),
            spacing3=10,
            lmargin1=10,
            lmargin2=10,
            rmargin=10,
            borderwidth=2,
            relief="ridge"
        )
        
        # AI (BLUE)
        self.chat_display._textbox.tag_config("ai_label",
            foreground="#58a6ff",
            font=("Segoe UI", 10, "bold"),
            spacing3=5
        )
        self.chat_display._textbox.tag_config("ai_bubble",
            background="#1a2a3a",
            foreground="#e6edf3",
            font=("Segoe UI", 12),
            spacing3=10,
            lmargin1=30,
            lmargin2=10,
            rmargin=10,
            borderwidth=2,
            relief="ridge"
        )
        
        self.chat_display._textbox.tag_config("system",
            foreground="#8b949e",
            font=("Segoe UI", 10),
            spacing3=5
        )
        self.chat_display._textbox.tag_config("error",
            foreground="#f85149",
            font=("Segoe UI", 10),
            spacing3=5
        )
        
        # ===== INPUT AREA =====
        self.input_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.input_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        input_container = ctk.CTkFrame(
            self.input_frame,
            fg_color="#1a1a2e",
            corner_radius=12,
            border_width=1,
            border_color="#2d3748"
        )
        input_container.pack(fill='x', padx=0, pady=0)
        
        self.input_field = ctk.CTkEntry(
            input_container,
            height=45,
            placeholder_text="Ask anything... (Press Enter to send)",
            font=ctk.CTkFont(size=13),
            fg_color="#0d1117",
            border_width=0,
            text_color="#e6edf3"
        )
        self.input_field.pack(side='left', fill='x', expand=True, padx=(12, 8), pady=8)
        self.input_field.bind('<Return>', self.send_message)
        
        send_btn = ctk.CTkButton(
            input_container,
            text="→",
            width=40,
            height=35,
            corner_radius=8,
            fg_color="#00ff88",
            hover_color="#00cc66",
            text_color="#000000",
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.send_message
        )
        send_btn.pack(side='right', padx=(0, 8), pady=8)
        
        self.start_time = datetime.now()
        self.update_timer()
        
        self.add_message("SYSTEM", "✨ Intellis AI ready. Type your question below.", "system")
        
        self.add_message("SYSTEM", "💬 Type any question — Get AI answers instantly", "system")
        self.add_message("SYSTEM", "📸 Full Screen Capture — Analyze anything on screen", "system")
        self.add_message("SYSTEM", "📐 Region Capture — Select specific area", "system")
        self.add_message("SYSTEM", "🎤 AI Answer — Auto-detect questions from audio", "system")
        self.add_message("SYSTEM", "👻 Stealth Mode — Dim overlay for meetings", "system")
        
    
    def update_timer(self):
        elapsed = datetime.now() - self.start_time
        minutes = int(elapsed.total_seconds() // 60)
        seconds = int(elapsed.total_seconds() % 60)
        self.timer_label.configure(text=f"{minutes:02d}:{seconds:02d}")
        self.root.after(1000, self.update_timer)
    
    def add_message(self, sender, text, msg_type="ai"):
        """Add formatted message with clear Q&A distinction"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Clear thinking indicator
        try:
            self.chat_display.delete("end-2l", "end-1l")
        except:
            pass
        
        if msg_type == "system":
            self.chat_display.insert('end', f"\n[{timestamp}] ⚡ {text}\n\n", "system")
            self.chat_display.see('end')
            return
        elif msg_type == "error":
            self.chat_display.insert('end', f"\n[{timestamp}] ❌ {text}\n\n", "error")
            self.chat_display.see('end')
            return
        elif msg_type == "user":
            self.chat_display.insert('end', f"\n[{timestamp}] ", "system")
            self.chat_display.insert('end', "🧑 YOU ASKED:\n", "user_label")
            self.chat_display.insert('end', f"{text}\n", "user_bubble")
            self.chat_display.insert('end', "\n", "system")
        elif msg_type == "ai":
            self.chat_display.insert('end', f"\n[{timestamp}] ", "system")
            self.chat_display.insert('end', "🤖 INTELLIS ANSWERED:\n", "ai_label")
            self.chat_display.insert('end', f"{text}\n", "ai_bubble")
            self.chat_display.insert('end', "\n", "system")
        else:
            return
        
        self.chat_display.see('end')
    
    def send_message(self, event=None):
        """Send message to AI with error handling"""
        question = self.input_field.get().strip()
        
        if not question:
            return
        
        self.input_field.delete(0, 'end')
        self.add_message("USER", question, "user")
        
        if not self.app:
            self.add_message("ERROR", "AI not connected. Please restart the app.", "error")
            return
        
        # Show thinking indicator
        self.chat_display.insert('end', "⏳ Thinking...\n\n")
        self.chat_display.see('end')
        self.root.update()
        
        try:
            answer = self.app.ai.process(question)
            
            # Remove thinking indicator
            self.chat_display.delete("end-2l", "end-1l")
            
            if "Error:" in answer or "503" in answer or "429" in answer or "404" in answer:
                self.add_message("ERROR", f"AI Error: {answer}", "error")
            else:
                self.add_message("AI", answer, "ai")
                
        except Exception as e:
            self.chat_display.delete("end-2l", "end-1l")
            self.add_message("ERROR", f"Error: {str(e)[:200]}", "error")
    
    def capture_full_screen(self):
        self.add_message("SYSTEM", "📸 Capturing full screen...", "system")
        self.root.update()
        thread = threading.Thread(target=self._do_full_screen_capture, daemon=True)
        thread.start()
    
    def _do_full_screen_capture(self):
        try:
            import pyautogui
            import os
            
            screenshot = pyautogui.screenshot()
            temp_path = "temp_capture.png"
            screenshot.save(temp_path)
            
            try:
                import pytesseract
                if hasattr(config, 'tesseract_path'):
                    pytesseract.pytesseract.tesseract_cmd = config.tesseract_path
                
                text = pytesseract.image_to_string(screenshot)
                
                if text and len(text.strip()) > 10:
                    self.add_message("SYSTEM", f"📝 Extracted {len(text)} characters", "system")
                    if self.app:
                        response = self.app.ai.process(text[:3000])
                        if "Error:" in response or "503" in response or "429" in response:
                            self.add_message("ERROR", f"AI Error: {response}", "error")
                        else:
                            self.add_message("AI", response, "ai")
                else:
                    self.add_message("ERROR", "No text found in screenshot.", "error")
            
            except ImportError:
                self.add_message("ERROR", "Tesseract not installed.", "error")
            except Exception as e:
                self.add_message("ERROR", f"OCR failed: {str(e)[:100]}", "error")
            
            try:
                os.remove(temp_path)
            except:
                pass
                
        except Exception as e:
            self.add_message("ERROR", f"Capture failed: {str(e)[:100]}", "error")
    
    def capture_region(self):
        self.add_message("SYSTEM", "📐 Position mouse and wait 3 seconds...", "system")
        self.root.update()
        thread = threading.Thread(target=self._do_region_capture, daemon=True)
        thread.start()
    
    def _do_region_capture(self):
        try:
            import pyautogui
            import time
            
            time.sleep(3)
            x, y = pyautogui.position()
            region = (x-200, y-100, 400, 200)
            screenshot = pyautogui.screenshot(region=region)
            
            try:
                import pytesseract
                if hasattr(config, 'tesseract_path'):
                    pytesseract.pytesseract.tesseract_cmd = config.tesseract_path
                text = pytesseract.image_to_string(screenshot)
                
                if text.strip():
                    self.add_message("SYSTEM", f"📝 Extracted: {text[:150]}...", "system")
                    if self.app:
                        response = self.app.ai.process(text)
                        if "Error:" in response or "503" in response or "429" in response:
                            self.add_message("ERROR", f"AI Error: {response}", "error")
                        else:
                            self.add_message("AI", response, "ai")
                else:
                    self.add_message("ERROR", "No text found in selected region", "error")
            except ImportError:
                self.add_message("ERROR", "Tesseract not installed", "error")
            except Exception as e:
                self.add_message("ERROR", f"OCR failed: {str(e)[:100]}", "error")
                
        except Exception as e:
            self.add_message("ERROR", f"Region capture failed: {str(e)[:100]}", "error")
    
    def toggle_listening(self):
        self.is_listening = not self.is_listening
        if self.is_listening:
            self.status_dot.configure(text="● LISTENING", text_color="#ff4444")
            self.add_message("SYSTEM", "🎤 Listening mode active", "system")
        else:
            self.status_dot.configure(text="● ACTIVE", text_color="#00ff88")
            self.add_message("SYSTEM", "🔇 Listening mode paused", "system")
    
    def copy_last_answer(self):
        import pyperclip
        try:
            last_text = self.chat_display.get("end-2l", "end-1l")
            if "🤖 INTELLIS ANSWERED" in last_text:
                import re
                clean_text = re.sub(r'\[.*?\]', '', last_text)
                pyperclip.copy(clean_text.strip())
                self.add_message("SYSTEM", "📋 Last answer copied", "system")
            else:
                self.add_message("ERROR", "No answer to copy", "error")
        except:
            self.add_message("ERROR", "No answer to copy", "error")
    
    def clear_messages(self):
        self.chat_display.delete(1.0, 'end')
        self.add_message("SYSTEM", "🧹 Session cleared", "system")
    
    def toggle_stealth(self):
        self.is_stealth = not self.is_stealth
        if self.is_stealth:
            self.root.attributes('-alpha', 0.35)
            self.stealth_btn.configure(text="👁️")
            self.add_message("SYSTEM", "👻 Stealth mode enabled", "system")
        else:
            self.root.attributes('-alpha', 0.88)
            self.stealth_btn.configure(text="👻")
            self.add_message("SYSTEM", "👁️ Stealth mode disabled", "system")
    
    def emergency_hide(self):
        self.root.attributes('-alpha', 0.0)
        self.add_message("SYSTEM", "⚠️ Emergency hide activated", "system")
    
    def toggle_input(self):
        self.input_field.focus()
    
    def quit(self):
        self.root.quit()
    
    def run(self):
        self.root.mainloop()