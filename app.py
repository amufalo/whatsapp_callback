from fastapi import FastAPI, Request
import base64
from glom import glom
import whatsapp
import dotenv
import ai

dotenv.load_dotenv()

app = FastAPI()

def base64_to_file(raw: str, filename: str):
    with open(filename, "wb") as fh:
        fh.write(base64.b64decode(raw))    

def process_voice_message(data,remote,message_id,session_id):
    filename="./media/"+message_id+".ogg"
    base64_to_file(data,filename)
    message="Transcrição do audio: \n"+ ai.transcription(filename)
    whatsapp.message_reply(session_id,message_id,remote,message)

def process_media(body):
    data = glom(body,"data.messageMedia.data")
    mimetype =  glom(body,"data.messageMedia.mimetype")
    remote = glom(body,"data.message.id.remote")
    message_id = glom(body,"data.message.id.id")
    session_id = glom(body,"sessionId")
    print(mimetype)
    if mimetype == "audio/ogg; codecs=opus":
        process_voice_message(data,remote,message_id,session_id)
 
@app.post("/callback")
async def callback(request: Request):
    body = await request.json()
    if ("dataType" in body):
        if body["dataType"] == "media":
            #print(body)
            process_media(body)
    