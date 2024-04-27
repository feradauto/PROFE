

def format_chat_history(chat):
  chat_str=""
  for message in chat:
    chat_str+=f"{message['role']}: {message['message']}\n"
  return chat_str