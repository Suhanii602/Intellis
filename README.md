<p align="center">
  <h1 align="center">✨ Intellis AI – Stealth Meeting Assistant</h1>
</p>

<p align="center">
  <strong>Real-time AI that stays invisible during screen shares</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/Platform-Windows-blueviolet.svg" alt="Platform">
  <img src="https://img.shields.io/badge/Status-Active-brightgreen.svg" alt="Status">
</p>

---

## 🚀 Features

- 💬 **AI Q&A** – Type any question, get instant answers
- 📸 **Full Screen Capture** – Analyze anything on screen
- 📐 **Region Capture** – Select specific area to analyze
- 🎤 **Voice Input** – Auto‑detect questions from audio
- 👻 **Stealth Mode** – Dim overlay during meetings
- 🔒 **Invisible During Screen Share** – Windows Display Affinity API
- 🧠 **Markdown Support** – Bold, italics, headings, code blocks in responses
- ⚡ **Real‑time** – Responses in a couple of seconds
- 🎨 **Modern UI** – Clean, dark-themed interface
- 🔄 **Cross-Platform** – Works with Zoom, Google Meet, Teams

---


## 🛠️ Installation

### Prerequisites

- Python 3.11 or higher
- Windows 10/11
- Tesseract OCR (for text extraction)

### Step 1: Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/intellis-ai.git
cd intellis-ai
```

### Step 2: Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate    # Windows
```

### Step 3: Install dependencies

```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
pip install git+https://github.com/openai/whisper.git
```

### Step 4: Configure API key

```bash
copy config_template.json config.json
```

Open `config.json` and add your Gemini API key:

```json
{
  "app": {
    "name": "Intellis AI"
  },
  "ai": {
    "provider": "gemini",
    "api_keys": {
      "gemini": "YOUR_GEMINI_API_KEY_HERE"
    }
  },
  "whisper": {
    "model": "base.en"
  },
  "paths": {
    "tesseract": "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
  }
}
```

Get your free API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

### Step 5: Install Tesseract OCR (Optional but recommended)

Download and install from: [Tesseract GitHub](https://github.com/UB-Mannheim/tesseract/wiki)

Default installation path: `C:\Program Files\Tesseract-OCR\tesseract.exe`

### Step 6: Choose Whisper model (Optional)

In `config.json`, change the `whisper.model` value:

| Model | Size | Accuracy | Speed | Recommended |
|-------|------|----------|-------|-------------|
| `tiny` | 75 MB | Lowest | Fastest | ❌ |
| `base.en` | 142 MB | Good | Fast | ✅ **Default** |
| `small` | 466 MB | Better | Medium | ✅ |
| `medium.en` | 1.5 GB | High | Slow | ⚠️ GPU recommended |
| `large` | 2.9 GB | Best | Slowest | ⚠️ GPU required |

### Step 7: Run the app

```bash
python src/main.py
```

---

## 🎤 Voice Input Setup (Optional)

To use the voice question detection feature:

### 1. Install Virtual Audio Cable

Download and install [VB-CABLE Virtual Audio Cable](https://vb-audio.com/Cable/)

### 2. Configure Windows Sound Settings

- Open **Sound Settings** (right-click speaker icon)
- Go to **Sound Control Panel**
- Under **Recording** tab, set "CABLE Output" as default communication device
- Under **Playback** tab, ensure your speakers are still default

### 3. Configure Your Meeting App

| App | Setting |
|-----|---------|
| **Zoom** | Settings → Audio → Microphone: "CABLE Input" |
| **Google Meet** | Settings → Audio → Microphone: "CABLE Input" |
| **Microsoft Teams** | Settings → Devices → Microphone: "CABLE Input" |

### 4. Enable Voice Input in Intellis

Click the 🎤 **Listen** button in the Intellis interface

---

## 📂 Project Structure

```
intellis-ai/
│
├── src/
│   ├── overlay.py           # UI and stealth logic
│   ├── ai_processor.py      # Gemini API integration
│   ├── config.py            # Configuration loader
│   ├── audio_processor.py   # Whisper speech-to-text
│   └── main.py              # Entry point
│
├── assets/
│   └── icon.ico             # Application icon
│
├── screenshots/
│   ├── local.png            # Local view screenshot
│   └── remote.png           # Remote view screenshot
│
├── config_template.json     # Template for API keys
├── requirements.txt         # Python dependencies
├── run_intellisai.py        # EXE entry point
├── README.md                # This file
├── LICENSE                  # MIT License
└── .gitignore               # Git ignore rules
```

---

## 🧠 Technologies Used

| Technology | Purpose | Version |
|------------|---------|---------|
| **Python** | Core language | 3.11+ |
| **CustomTkinter** | Modern UI framework | 5.2.0 |
| **Google Gemini API** | AI reasoning & Q&A | 0.3.0 |
| **OpenAI Whisper** | Speech‑to‑text | Latest |
| **Tesseract OCR** | Screen text extraction | 5.3.0 |
| **Pillow** | Image processing | 10.0.0 |
| **PyGetWindow** | Window management | 0.0.9 |
| **Keyboard** | Global hotkeys | 0.13.5 |
| **PyInstaller** | EXE packaging | 6.0.0 |
| **Windows Display Affinity** | Screen‑share invisibility | Native |

---

## 🔧 Configuration Options

### Complete `config.json` Reference

```json
{
  "app": {
    "name": "Intellis AI",
    "version": "1.0.0",
    "theme": "dark"
  },
  "ai": {
    "provider": "gemini",
    "api_keys": {
      "gemini": "YOUR_GEMINI_API_KEY_HERE"
    },
    "model": "gemini-1.5-flash",
    "temperature": 0.7,
    "max_tokens": 500
  },
  "whisper": {
    "model": "base.en",
    "language": "en",
    "device": "cpu",
    "compute_type": "int8"
  },
  "paths": {
    "tesseract": "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
  },
  "hotkeys": {
    "toggle_visibility": "ctrl+alt+h",
    "capture_full": "ctrl+alt+f",
    "capture_region": "ctrl+alt+r",
    "voice_input": "ctrl+alt+v"
  },
  "overlay": {
    "opacity": 0.92,
    "border_radius": 10,
    "width": 600,
    "height": 400,
    "stealth_mode": true
  }
}
```

---

## 🎯 Use Cases

| Scenario | How Intellis AI Helps |
|----------|----------------------|
| **Technical Interviews** | Get instant code snippets and explanations |
| **Sales Demos** | Answer client questions on the fly |
| **Remote Presentations** | Look up data without leaving the meeting |
| **Team Collaboration** | Quickly verify information during discussions |
| **Training Sessions** | Provide instant examples and references |
| **Brainstorming** | Generate ideas without breaking flow |

---

## 🔒 Privacy & Security

- 🔐 **No Data Storage** – All data is processed in memory, never saved
- 🌐 **API Only** – Only communicates with Google Gemini API
- 👻 **Stealth Mode** – Your activity remains hidden from meeting participants
- 🔑 **Local Keys** – API keys stored locally on your machine
- 📡 **No Telemetry** – No usage tracking or analytics

---

## ❓ Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| **Overlay not showing** | Check `config.json` paths, ensure Tesseract is installed |
| **API key errors** | Verify Gemini API key in `config.json`, check billing status |
| **Voice not working** | Ensure VB-CABLE is installed and configured properly |
| **Screen capture fails** | Run as administrator, check screen permissions |
| **Slow responses** | Switch to a lighter Whisper model (e.g., `base.en`) |

### Quick Fixes

```bash
# Reinstall dependencies
pip install --force-reinstall -r requirements.txt

# Reset configuration
copy config_template.json config.json

# Run with debug logging
python src/main.py --debug
```

---

## 🚧 Roadmap

- [x] Basic Q&A functionality
- [x] Screen capture integration
- [x] Voice input support
- [x] Stealth mode
- [ ] MacOS support
- [ ] Linux support
- [ ] Multiple language support
- [ ] Custom AI models
- [ ] Browser extension
- [ ] Mobile companion app

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### Development Setup

```bash
# Fork and clone
git clone https://github.com/YOUR_USERNAME/Intellis.git
cd intellis-ai

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Format code
black src/
```

### Contribution Guidelines

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/NewFeature`)
3. Commit your changes (`git commit -m 'Add some NewFeature'`)
4. Push to the branch (`git push origin feature/NewFeature`)
5. Open a Pull Request

### Code Style

- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings for functions
- Write unit tests for new features
- Update documentation accordingly

---

## 📄 License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.

```
MIT License

Copyright (c) 2024 Your Name

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🙏 Acknowledgements

- [OpenAI Whisper](https://github.com/openai/whisper) – Speech recognition
- [Google Gemini](https://deepmind.google/technologies/gemini/) – AI responses
- [CustomTkinter](https://customtkinter.tomschimansky.com/) – Modern UI
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) – Text extraction
- [VB-CABLE](https://vb-audio.com/Cable/) – Virtual audio routing
- [Font Awesome](https://fontawesome.com/) – Icons and emojis
- [PyInstaller](https://pyinstaller.org/) – EXE packaging

---

## 📬 Contact

**Suhani Shrivastava**  
- 📧 Email: shrivastava.suhani06@gmail.com
  
**Project Link:** [https://github.com/Suhanii602/Intellis](https://github.com/Suhanii602/Intellis)

---

## ⭐ Star History

If you find Intellis AI useful, please consider giving it a star! ⭐

[![Star History Chart](https://api.star-history.com/svg?repos=YOUR_USERNAME/intellis-ai&type=Date)](https://star-history.com/#YOUR_USERNAME/intellis-ai&Date)

---

<p align="center">
  <b>Made with ❤️ and lots of ☕</b><br>
  <sub>© 2024 Intellis AI. All rights reserved.</sub>
</p>
