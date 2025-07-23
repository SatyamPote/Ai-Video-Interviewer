import flask
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from gradio_client import Client, handle_file
from gtts import gTTS
import os
import datetime
import speech_recognition as sr
from pydub import AudioSegment
import sys

# ==============================================================================
# HARD-CODED FFMPEG PATHS (PLAN B)
# This explicitly tells the pydub library where to find the ffmpeg executables.
# This should be the definitive fix for the audio processing error.
# The 'r' before the string is important to handle backslashes correctly.
# ==============================================================================
try:
    AudioSegment.converter = r"C:\ffmpeg\bin\ffmpeg.exe"
    AudioSegment.ffprobe = r"C:\ffmpeg\bin\ffprobe.exe"
    print("✅ FFmpeg paths successfully set in Pydub.")
except Exception as e:
    print(f"⚠️ Warning: Could not set FFmpeg paths. Pydub might not work. Error: {e}")

# --- Initialize Flask App and CORS ---
app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app, resources={r"/*": {"origins": "*"}})

# --- Initialize Gradio Client with Error Handling ---
try:
    print("Attempting to connect to Hugging Face AI model...")
    client = Client("ahmedatk/ai_interviewer")
    print("✅ Connection to Hugging Face successful!")
except Exception as e:
    print("---------------------------------------------------------------")
    print(f"❌ FATAL ERROR: Could not connect to the Hugging Face API.")
    print(f"   Error details: {e}")
    print("   This is likely a network issue (firewall, slow connection) or the HF Space is down.")
    print("   The application cannot run without this connection. Exiting.")
    print("---------------------------------------------------------------")
    sys.exit(1)

# --- Helper Functions ---
def text_to_speech(text, filename_prefix="response"):
    """Converts text to an MP3 file and returns its URL."""
    audio_folder = os.path.join(app.static_folder, 'audio')
    os.makedirs(audio_folder, exist_ok=True)
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{filename_prefix}_{timestamp}.mp3"
    filepath = os.path.join(audio_folder, filename)
    
    cleaned_text = text.replace('**', '')
    if not cleaned_text.strip():
        cleaned_text = "I did not get a response."
        
    tts = gTTS(text=cleaned_text, lang='en', slow=False)
    tts.save(filepath)
    return f"/static/audio/{filename}?v={timestamp}"

# --- API Endpoints ---
@app.route('/')
def index():
    """Serves the main HTML page."""
    return render_template('index.html')

@app.route('/start-interview', methods=['POST'])
def start_interview():
    """Starts the interview using the Gradio client on the server."""
    if 'resume' not in request.files or 'job_desc' not in request.form:
        return jsonify({"error": "Missing resume or job description"}), 400

    resume_file = request.files['resume']
    job_desc = request.form['job_desc']
    
    temp_resume_path = f"temp_{os.path.basename(resume_file.filename)}"
    resume_file.save(temp_resume_path)
    
    try:
        result = client.predict(
            resume=handle_file(temp_resume_path),
            job_desc=job_desc,
            api_name="/gradio_start_interview"
        )
    except Exception as e:
        return jsonify({"error": f"Failed to communicate with AI: {e}"}), 500
    finally:
        os.remove(temp_resume_path)
    
    conversation_text = result[0]
    first_question = conversation_text.splitlines()[-1]
    audio_url = text_to_speech(first_question, "question_0")
    
    return jsonify({"conversation": conversation_text, "audio_url": audio_url})

@app.route('/process-response', methods=['POST'])
def process_response():
    """Transcribes user audio and gets the next AI response."""
    if 'audio' not in request.files or 'conversation_history' not in request.form:
        return jsonify({"error": "Missing audio or conversation history"}), 400

    audio_file = request.files['audio']
    conversation_history = request.form['conversation_history']
    
    # 1. Transcribe audio to text
    try:
        input_filename = "temp_user_audio.webm"
        wav_filename = "temp_user_audio.wav"
        audio_file.save(input_filename)
        AudioSegment.from_file(input_filename).export(wav_filename, format="wav")
        
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_filename) as source:
            audio_data = recognizer.record(source)
            user_response_text = recognizer.recognize_google(audio_data)
    except Exception as e:
        print(f"Audio Processing Error: {e}")
        # This error message should no longer appear with the hard-coded paths.
        user_response_text = "(Error processing audio. Please check server logs.)"
    finally:
        if os.path.exists(input_filename): os.remove(input_filename)
        if os.path.exists(wav_filename): os.remove(wav_filename)

    # 2. Get next AI response
    try:
        result = client.predict(response=user_response_text, api_name="/gradio_handle_response")
    except Exception as e:
        return jsonify({"error": f"Failed to communicate with AI: {e}"}), 500

    ai_full_response = result[0]
    new_ai_part = ai_full_response.split(user_response_text, 1)[-1].strip()
    audio_url = text_to_speech(new_ai_part, "question")
    
    updated_conversation = conversation_history + f"\n\n**You:** {user_response_text}\n\n{new_ai_part}"

    return jsonify({
        "conversation": updated_conversation,
        "audio_url": audio_url,
        "transcription": user_response_text,
        "ai_response": new_ai_part
    })


if __name__ == '__main__':
    print("Starting Flask server...")
    print("This server will connect to the Hugging Face AI and process audio.")
    app.run(debug=False, port=5001)