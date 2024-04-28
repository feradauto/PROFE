from datetime import datetime
messages = {}
collections = {}
def write_message_to_db(form_data, role):
    whatsapp = form_data['From']
    data={'student':whatsapp, 'message':form_data['Body'], 'role':role, 'message_type':'text', 'timestamp':datetime.now()}
    if whatsapp not in messages:
        messages[whatsapp] = [data]
    else:
        messages[whatsapp].append(data)

def read_message_from_db(student):
    if student in messages:
       return messages[student]
    else:
        return []

def write_collection_to_db(data, whatsapp, collection, subtopic):
    if whatsapp not in collections:
        collections[whatsapp] = {collection: [data]}
    else:
        if collection not in collections[whatsapp]:
            if subtopic not in collections[whatsapp][collection]:
                collections[whatsapp][collection][subtopic].append(data)
            else:
                collections[whatsapp][collection][subtopic] = [data]
        else:
            collections[whatsapp][collection] = {subtopic: [data]}
    return True

def read_collection_from_db(whatsapp, collection):
    if whatsapp in collections:
        if collection in collections[whatsapp]:
            return collections[whatsapp][collection]
    return []

def read_collections_from_db(whatsapp):
    if whatsapp in collections:
        return collections[whatsapp]
    return []