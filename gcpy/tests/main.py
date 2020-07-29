from gcpy.firestore.Document import Document as FirestoreDocument


def test_annotation():
    """
    Asserts that all fields are listed in the __init__
    """
    ann = set(FirestoreDocument.__annotations__)
    fields = [f.name for f in FirestoreDocument.fields]
    for field in fields:
        if not ann.__contains__(field):
            print('{} is missing in annotations'.format(field))
