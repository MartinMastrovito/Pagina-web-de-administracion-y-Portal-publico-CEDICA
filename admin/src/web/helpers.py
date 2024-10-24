from flask import current_app

def document_url(document):
    client = current_app.storage.client
    
    if document is None:
        return ""

    return client.presigned_get_object("grupo30", document)