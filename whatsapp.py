import requests
import os
import base64
import mimetypes

whatsapp_host=os.environ["WHATSAPP_HOST"]
whatsapp_key=os.environ["WHATSAPP_KEY"]


def message_reply(session_id: str, message_id: str, chat_id: str, content: str):
    url=whatsapp_host+"message/reply/"+session_id
    data = {
      "chatId": chat_id,
      "messageId": message_id,
      "contentType": "string",
      "content": content
    }
    header= {
      "x-api-key": whatsapp_key
    }
    resp=requests.post(url=url, headers=header, json=data)
    if resp.status_code !=200:
        print(resp.content)

def send_messagemedia(session_id: str, chat_id: str, file: str):
    
    with open(file, "rb") as f:
        file_data = f.read()
        file_base64 = base64.b64encode(file_data).decode('utf-8')
    
    with open(file+".txt", "w") as fh:
        fh.write(file_base64)    

    # Obtém informações do arquivo
    mimetype = mimetypes.guess_type(file)[0] or "application/octet-stream"
    filename = os.path.basename(file)
    filesize = os.path.getsize(file)
    if mimetype=="audio/ogg":
        mimetype=mimetype+"; codecs=opus"
    # Preenche o dicionário content
    content = {
        "mimetype": mimetype,
        "data": file_base64,
        "filename": filename
    }

    url=whatsapp_host+"client/sendMessage/"+session_id

    data = {
      "chatId": chat_id,
      "contentType": "MessageMedia",
      "content": content
    }
    header= {
      "x-api-key": whatsapp_key
    }
    print(data)
    print(url)
    resp=requests.post(url=url, headers=header, json=data)
    if resp.status_code !=200:
        print(resp.content)

