# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 12:34:32 2024

@author: USER
"""
        
from fastapi import FastAPI, UploadFile, File, HTTPException
import speech_recognition as sr

app = FastAPI()

def transcribe_audio(file_path, language='en-IN'):
    try:
        # Create a recognizer instance
        recognizer = sr.Recognizer()
        
        # Load audio file
        with sr.AudioFile(file_path) as source:
            audio_data = recognizer.record(source)
        
        # Use Google Speech Recognition to transcribe the audio
        text = recognizer.recognize_google(audio_data, language=language)
        return text
    except sr.UnknownValueError:
        # Handle unknown value error
        return "Google Speech Recognition could not understand the audio"
    except sr.RequestError as e:
        # Handle request error
        return f"Could not request results from Google Speech Recognition service; {e}"

@app.post("/speech_text")
async def speech_text(file: UploadFile = File(...), language: str = 'bn-IN'):
    print("Content Type:", file.content_type)  # Print content type
    if file.content_type.split('/')[0] != 'audio':
        raise HTTPException(status_code=400, detail="Uploaded file must be an audio file")

    try:
        # Save the uploaded file temporarily
        with open("temp_audio.wav", "wb") as buffer:
            buffer.write(file.file.read())

        # Transcribe the audio from the saved file
        text = transcribe_audio("temp_audio.wav", language=language)

        # Delete the temporary file
        os.remove("temp_audio.wav")

        return {"transcribed_text": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
