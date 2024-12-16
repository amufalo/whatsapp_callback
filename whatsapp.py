import requests
import os
import base64
import mimetypes

whatsapp_host=os.environ["WHATSAPP_HOST"]
whatsapp_key=os.environ["WHATSAPP_KEY"]


def message_reply(session_id: str, message_id: str, chat_id: str, content):
    url=whatsapp_host+"message/reply/"+session_id
    data = {
      "chatId": chat_id,
      "messageId": message_id,
      "content": content
    }
    header= {
      "x-api-key": whatsapp_key
    }
    print(data)
    print(url)
    requests.post(url=url, headers=header, data=data)

def message_reply_str(session_id: str, message_id: str, chat_id: str, content: str):
    message_reply(session_id, message_id, chat_id, content) 

def message_reply_media(session_id: str, message_id: str, chat_id: str, file: str):
    
    with open(file, "rb") as f:
        file_data = f.read()
        file_base64 = base64.b64encode(file_data).decode('utf-8')
    
    # Obtém informações do arquivo
    mimetype = mimetypes.guess_type(file)[0] or "application/octet-stream"
    filename = os.path.basename(file)
    filesize = os.path.getsize(file)

    # Preenche o dicionário content
    content = {
        "mimetype": mimetype,
        "data": file_base64,
        "filename": filename,
        "filesize": filesize
    }

    message_reply(session_id, message_id, chat_id, content) 

