from openai import OpenAI
import dotenv
import os


api_key=os.environ["OPENAI_API_KEY"]
client = OpenAI(api_key=api_key)

def transcription(filename: str) -> str:
    audio_file=open(filename, "rb")
    engine = client.audio.transcriptions.create(
      model="whisper-1", 
      file=audio_file
    )
    return engine.text