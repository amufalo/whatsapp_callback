from fastapi import FastAPI, Request
import base64
from glom import glom
import whatsapp
import dotenv
import ai
from pdf_to_audio import pdf_to_audio

dotenv.load_dotenv()

app = FastAPI()

def base64_to_file(raw: str, filename: str):
    with open(filename, "wb") as fh:
        fh.write(base64.b64decode(raw))    

def process_voice_message(data,remote,message_id,session_id):
    filename="./media/"+message_id+".ogg"
    base64_to_file(data,filename)
    message="Transcrição do audio: \n"+ ai.transcription(filename)
    whatsapp.message_reply_str(session_id,message_id,remote,message)

def process_pdf(data,remote,message_id,session_id):
    filename="./media/"+message_id+".pdf"
    base64_to_file(data,filename)    
    ok, files = pdf_to_audio(filename,"./media/"+message_id+"/")
    if ok:
        total=len(files)
        whatsapp.message_reply_str(session_id,message_id,remote,f"O retorno será em *${total}* partes")
        for i,str in enumerate(files):
            whatsapp.message_reply_str(session_id,message_id,remote,f"*Parte {i}*")
            whatsapp.message_reply_media(session_id,message_id,remote,str)
    else:
        whatsapp.message_reply_str(session_id,message_id,remote,f"Não foi possível extrair texto do PDF")


def process_media(body):
    data = glom(body,"data.messageMedia.data")
    mimetype =  glom(body,"data.messageMedia.mimetype")
    remote = glom(body,"data.message.id.remote")
    message_id = glom(body,"data.message.id.id")
    session_id = glom(body,"sessionId")
    if mimetype == "audio/ogg; codecs=opus":
        process_voice_message(data,remote,message_id,session_id)
    elif mimetype == "application/pdf":
        process_pdf(data,remote,message_id,session_id)
 
@app.post("/callback")
async def callback(request: Request):
    body = await request.json()
    if ("dataType" in body):
        if body["dataType"] == "media":
            process_media(body)
    