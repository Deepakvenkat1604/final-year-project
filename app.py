from flask import Flask, render_template, request, jsonify
import os
from keybert import KeyBERT
import openai
import time
import torch
import soundfile as sf
from pydub import AudioSegment
import whisper
from datetime import datetime
import speech_recognition as sr
from whisper_utils import transcribe_audio  # Import Whisper function

from keybert import KeyBERT
from sentence_transformers import SentenceTransformer
# Use a pipeline as a high-level helper
from transformers import pipeline
# Load model directly
from transformers import AutoTokenizer, AutoModelForPreTraining

tokenizer = AutoTokenizer.from_pretrained("law-ai/InLegalBERT")
model = AutoModelForPreTraining.from_pretrained("law-ai/InLegalBERT")
pipe = pipeline("fill-mask", model="law-ai/InLegalBERT")
# Load a legal-specific transformer for better results
 # Load InLegalBERT
kw_model = KeyBERT(model) 
# import OpenAI from "openai";
# const client = new OpenAI();
# client = openai.OpenAI(api_key="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")
# models = client.models.list()
# for model in models.data:
#     print(model.id)
#query = "What are the tax exemptions for startups under the Indian Income Tax Act?"
#keywords = kw_model.extract_keywords(query, keyphrase_ngram_range=(1,3), stop_words="english", top_n=10)

#print("Extracted Keywords:", keywords)

# import spacy

# # Load a pre-trained NER model for legal texts
# nlp = spacy.load("nlpaueb/legal-bert-base-uncased")  # Free model trained on legal text


# text = "Are there any capital gains tax exemptions under section 54 of the Income Tax Act?"
# doc = nlp(text)

# keywords = [ent.text for ent in doc.ents]  # Extract named entities
# print("Extracted Keywords:", keywords)

# from transformers import pipeline

# generator = pipeline("text-generation", model="mistralai/Mistral-7B-Instruct")
# query = "What are the tax benefits for small businesses under Indian law?"

# prompt = f"Extract tax-related keywords from this: {query}"
# response = generator(prompt, max_length=50)

# print("Extracted Keywords:", response)


# kw_model = KeyBERT("sentence-transformers/all-MiniLM-L6-v2")
TAX_KEYWORDS = {"tax", "gst", "income", "deduction", "exemption", "refund", "section", "act", "law", "finance", "return", "penalty", "capital gains", "investment", "rebate"}
#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
app = Flask(__name__, template_folder="templates", static_folder="static")

UPLOAD_FOLDER = "uploads1"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


model = whisper.load_model("base")

@app.route('/')
def index():
    return render_template("index.html", result=None, transcribed_text=None, keywords=None)

@app.route('/process', methods=['POST'])
def process():
    text_input = request.form.get("text_input", "")
    if not text_input:
        return render_template("index.html", result="No input provided!", transcribed_text=None,keywords=None)

    # Placeholder for tax law search
    print(f"Text input: {text_input}")  # Debugging
    # Extract keywords using KeyBERT
    keywords = kw_model.extract_keywords(text_input, keyphrase_ngram_range=(1,3), stop_words="english", top_n=12)
    
    # Filter keywords to keep only relevant tax-related terms
    filtered_keywords = [kw for kw, score in keywords if any(term in kw.lower() for term in TAX_KEYWORDS)]
    if not filtered_keywords:
        filtered_keywords = ["Not found"]
    print(f"Filtered keywords: {filtered_keywords}")  # Debugging
#     prompt = f"Extract Indian tax law keywords from this query: '{text_input}'. Return as a comma-separated list."
   
#     response = client.chat.completions.create(
#     model="gpt-4o",
#     messages=[{"role": "user", "content": prompt}],
#     temperature=0.3,
#     max_tokens=50
# )

#     gpt_keywords_text = response.choices[0].message.content
#     keywords = [kw.strip() for kw in gpt_keywords_text.split(",")]
    # Placeholder for tax law search result
    result = f"Searching for relevant tax laws related to: {text_input}"
    
    return render_template("index.html", result=result, transcribed_text=text_input, keywords=filtered_keywords)    
   
@app.route('/voice_process', methods=['POST'])
def voice_process():
        transcription = request.form.get("voiceText", "")
        print(f"Text input: {transcription}")  # Debugging
        # prompt = f"Extract Indian tax law keywords from this query: '{transcription}'. Return as a comma-separated list."
        # response = openai.ChatCompletion.create(
        # model="gpt-4",  # or "gpt-3.5-turbo"
        # messages=[{"role": "user", "content": prompt}],
        # temperature=0.3,
        # max_tokens=50
        # )
        # keywords_text = response["choices"][0]["message"]["content"]
        # keywords = [kw.strip() for kw in keywords_text.split(",")]
        if not transcription:
            return render_template("index.html", result="No transcription provided!", transcribed_text=None, keywords=None)

        # Extract keywords using KeyBERT
        keyword = kw_model.extract_keywords(transcription, keyphrase_ngram_range=(1,2), stop_words="english", top_n=12)

        # Filter keywords to keep only relevant tax-related terms
        filtered_keywords = [kw for kw, score in keyword if any(term in kw.lower() for term in TAX_KEYWORDS)]
        if not filtered_keywords:
            filtered_keywords = ["Not found"]
        print(f"Filtered keywords: {filtered_keywords}")  # Debugging

        # Placeholder for tax law search result
        result = f"Searching for relevant tax laws related to: {transcription}"
        return jsonify({ "filtered_keywords": filtered_keywords, "result": result,"transcribed_text": transcription})

       # return render_template("index.html", result=result, voice_text=transcription, keywords=filtered_keywords)
      

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if "audio" not in request.files:
        print("No audio file")
        return jsonify({"error": "No audio file"}), 400

    audio_file = request.files["audio"]
    if audio_file.filename == "":
        print("No selected file")
        return jsonify({"error": "No selected file"}), 400
    print(f"Received audio: {audio_file}")  # Debugging
    #filename = f"recorded_audio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.webm"
    file_path = os.path.join(UPLOAD_FOLDER,audio_file.filename)
    
    # Save the file
    audio_file.save(file_path)
    original_audio_path = file_path
    converted_audio_path = os.path.join(UPLOAD_FOLDER, "converted_audio.wav")
    # original_audio_path = os.path.join(UPLOAD_FOLDER, audio_file.filename)
    # converted_audio_path = os.path.join(UPLOAD_FOLDER, "converted_audio.wav")    

    try:
        audio_file.save(original_audio_path)
        print(f"Saved audio: {original_audio_path}")  # Debugging: Check if file is saved correctly
        # Convert audio to WAV format (PCM encoding)
        # if not os.path.exists(original_audio_path):
        #     print(f"File not found after saving: {original_audio_path}")
        #     return jsonify({"error": "File not saved"}), 500
        # print("Converting audio to WAV...")  # Debugging
        # audio = AudioSegment.from_file(audio_file)

        # audio.export(converted_audio_path, format="wav")
        # print(f"Converted audio to WAV: {converted_audio_path}")  # Debugging
        # try:
        #     data, samplerate = sf.read(converted_audio_path)  # Check if file is readable
        #     print(f"Audio format verified: {samplerate} Hz")
        # except Exception as e:
        #     print(f"Invalid audio format: {str(e)}")
        #     return jsonify({"error": "Invalid audio format"}), 500
        # Use Whisper AI for transcription
        transcribed_text = model.transcribe("uploads1/harvard.wav")["text"]
        print(f"Whisper Transcription: {transcribed_text}")  # Debugging
        return jsonify({"transcription": transcribed_text})

    except Exception as e:
        print(f"Whisper failed: {str(e)}")  # Debugging
        return jsonify({"error": "Failed to process audio", "details": str(e)}), 500
    
    finally:
        # Clean up temporary files
        if os.path.exists(original_audio_path):
            os.remove(original_audio_path)
        if os.path.exists(converted_audio_path):
            os.remove(converted_audio_path)
        # Fallback to Google Speech Recognition
    #     recognizer = sr.Recognizer()
    #     with sr.AudioFile(audio_path) as source:
    #         audio_data = recognizer.record(source)
        
    #     try:
    #         transcribed_text = recognizer.recognize_google(audio_data)
    #         print(f"Google Speech Transcription: {transcribed_text}")  # Debugging
    #     except sr.UnknownValueError:
    #         transcribed_text = "Could not understand the audio."
    #     except sr.RequestError:
    #         transcribed_text = "Could not connect to Google Speech API."

    # return jsonify({"transcription": transcribed_text})


if __name__ == '__main__':
    app.run(debug=True)
