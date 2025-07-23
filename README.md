# 🤖 AI Video Interviewer

An immersive, AI-powered mock interview platform that simulates a real-time video call experience. This application helps users practice for job interviews by providing dynamic, job-specific questions, transcribing spoken answers, and delivering the AI’s responses with audible speech.

![Demo GIF of the AI Interviewer in action](link-to-your-demo.gif)  
*(Replace this with a demo GIF showing your app in action)*

---

## ✨ Features

- 🧠 Dynamic AI-powered interview questions using Hugging Face ([ahmedatk/ai_interviewer](https://huggingface.co/spaces/ahmedatk/ai_interviewer))
- 🎙️ Speech Recognition with `SpeechRecognition`
- 🔊 Text-to-Speech via `gTTS` and `pydub` (requires FFmpeg)
- 💬 Interactive chat UI with separate bubbles for user and interviewer
- 📁 Upload resume and job description for personalized sessions
- ⚙️ Built with Python/Flask backend and HTML/CSS/JavaScript frontend

---

## 🛠️ Tech Stack

| Layer            | Technology Used                             |
|------------------|---------------------------------------------|
| Backend          | Python, Flask, Flask-Cors                   |
| Frontend         | HTML5, CSS3, JavaScript                     |
| AI Integration   | Hugging Face Spaces, `gradio_client`        |
| Speech-to-Text   | `SpeechRecognition`                         |
| Text-to-Speech   | `gTTS`, `pydub`, FFmpeg                     |

---

## 🔧 Setup Instructions

### Prerequisites

- Python 3.8+
- FFmpeg (audio processing)

### FFmpeg Installation

- **Windows**: [Download here](https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip) → extract → add `bin/` to system PATH  
- **macOS**: `brew install ffmpeg`  
- **Linux**: `sudo apt-get install ffmpeg`  

To verify:  
```bash
ffmpeg -version
```

### Installation Steps

```bash
# Clone the repository
git clone https://github.com/your-username/ai-video-interviewer.git
cd ai-video-interviewer

# Create a virtual environment
python -m venv venv

# Activate it
source venv/bin/activate        # macOS/Linux
.\venv\Scripts\activate         # Windows

# Install Python dependencies
pip install Flask Flask-Cors gradio_client gTTS SpeechRecognition pydub

# Run the Flask app
python app.py
```

---

## 📋 How to Use

1. Visit `http://127.0.0.1:5001` in your browser.
2. Grant permission for webcam and microphone.
3. Upload your resume (PDF) and paste job description.
4. Click **Start Interview**.
5. The AI will speak a question aloud.
6. Click **Record Answer**, speak your response, then **Stop Recording**.
7. Your answer will be transcribed and sent back to the AI.
8. The AI replies and continues the dialogue.

---

## 📁 Project Structure

```
ai-video-interviewer/
├── app.py                   # Flask backend server
├── templates/
│   └── index.html           # Web interface
├── static/
│   ├── style.css            # CSS styling
│   ├── script.js            # Client-side JavaScript
│   ├── assets/
│   │   └── ai_visual.png    # Visual avatar for AI
│   └── audio/               # Folder for generated speech
├── README.md                # Project documentation
└── requirements.txt         # Python dependencies
```

---

## ❗ Troubleshooting

- **FFmpeg Audio Error:**  
  If you see `Error processing audio. Is FFmpeg correctly installed?`, ensure FFmpeg is in your system’s PATH. Verify by running `ffmpeg -version`.

- **API Model Unreachable:**  
  If Hugging Face returns a connection error, check your internet connection or firewall settings. Retry later if the model is temporarily offline.

---

## 🚀 Future Plans

- [ ] Voice tone and clarity analysis for user responses  
- [ ] Multiple AI personalities and accents  
- [ ] Save and replay previous interviews  
- [ ] Generate interview performance reports  
- [ ] Resume parsing and automatic job-specific questions

---

## 📄 License

This project is licensed under the MIT License.  
See `LICENSE.md` for full terms and conditions.

---

## 🙌 Acknowledgments

- Hugging Face model: [`ahmedatk/ai_interviewer`](https://huggingface.co/spaces/ahmedatk/ai_interviewer)  
- Libraries: Flask, gTTS, SpeechRecognition, pydub, gradio_client  
- Audio: FFmpeg for TTS conversion  
- Contributors and the open-source community for making this possible.

---

## 🎨 Bonus Branding Tip

Consider adding a branded logo and tagline, such as:

> **Qedence** – “Interview smarter. Speak bolder.”

You can include this at the top of the interface or as the favicon to solidify your project's identity.

---
