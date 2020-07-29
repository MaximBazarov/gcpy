from gcpy.firestore.Collection import db


def generate_collection_class(
        collection: str,
        doc_id: str,
        class_names_prefix: str
):

    doc_ref = db.target_collection(collection).document(doc_id).get()
    if not doc_ref:
        raise ValueError("There's no {} in {}".format(doc_id, collection))
    doc = doc_ref.to_dict()

    print('from datetime import datetime')
    # DatetimeWithNanoseconds
    imp = ''
    for field in doc.keys():
        t = type(doc[field]).__name__
        if t == 'DatetimeWithNanoseconds':
            imp = 'from google.api_core.datetime_helpers import DatetimeWithNanoseconds'
    if imp:
        print(imp)

    print()

    print("class {}Document(Document):".format(class_names_prefix))

    for field in doc.keys():
        t = type(doc[field]).__name__
        if t == 'int':
            t = 'float'
        print('    {}: {}'.format(field, t))
    print('\n    fields = [')
    for field in doc.keys():
        t = type(doc[field]).__name__
        if t == 'int' or t == 'float':
            t = 'number'
        if t == 'DatetimeWithNanoseconds':
            t = 'datetime'
        if t == 'str':
            t = 'string'

        print('        DocumentField(')
        print('            name=\'{}\','.format(field))
        print('            field_type=FieldType.{}()'.format(t))
        print('        ),')
    print('    ]')

    print()
    print("class {}Collection(FirestoreCollection):".format(class_names_prefix))
    print("    name = '{}'".format(collection))
    print("    document_type = {}Document".format(class_names_prefix))
