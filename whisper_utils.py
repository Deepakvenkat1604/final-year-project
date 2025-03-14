import whisper
import os
import speech_recognition as sr
os.environ["PATH"] += os.pathsep + os.path.dirname(r"C:\Users\Deepa\OneDrive\Desktop\final_year_project\.venv\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe")

# Load Whisper model globally (faster performance)
model = whisper.load_model("base")  # You can use "small", "medium", or "large"

def transcribe_audio(audio_path):
    recognizer = sr.Recognizer()
    
    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)
    
    try:
        text = recognizer.recognize_google(audio_data)
        return text
    except sr.UnknownValueError:
        return "Could not understand the audio"
    except sr.RequestError:
        return "Could not connect to Google Speech API"
