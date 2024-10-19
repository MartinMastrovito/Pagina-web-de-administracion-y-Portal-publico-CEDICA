from flask import current_app

def document_url(document):
    client = current_app.storage.client
    
    if document is None:
        return ""
    
    aux = client.presigned_get_object("grupo30", document)
    
    print(aux)
    
    return aux