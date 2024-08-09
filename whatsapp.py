import requests

BASE_URL="http://192.168.15.34:3000/"

def message_reply(session_id: str, message_id: str, chat_id: str, content: str):
    url=BASE_URL+"message/reply/"+session_id
    data = {
  "chatId": chat_id,
  "messageId": message_id,
  "content": content
}
    requests.post(url=url,data=data)
