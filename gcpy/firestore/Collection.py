from google.cloud import firestore
from google.cloud.firestore_v1beta1 import DocumentReference

from gcpy.firestore.Document import Document

db = firestore.Client()


class FirestoreCollection:
    name = ''
    """
    Collection name
    """

    document_type = Document.__class__
    """
    Document type
    """

    asc = 'ASCENDING'
    desc = 'DESCENDING'

    @classmethod
    def transaction(cls):
        return db.transaction()

    @classmethod
    def save(cls, document: Document, doc_id: str = None, merge: bool = False):
        """
        Saves `document` into the collection

        Args:
            document: Document
            doc_id: Id or None, will be autogenerated if None
            merge: Should it merge the data if document exists

        Returns:

        """
        if doc_id is None:
            doc_id = document.id
        obj = dict(document)
        if obj:
            cls._save(obj, doc_id, merge)

    @classmethod
    def _save_list(cls, objects_list: list, merge: bool = False):
        """
        Batch save the list of object into collection_to_listen
        tries to save with chunks of 500 items

        :param objects_list: list of objects of type object, each must have an id field
        :param merge: should the object be merged with that is already exists in the database
        """
        collection = cls.name
        if not collection or not isinstance(objects_list, list):
            return
        batch = db.batch()
        counter = 0
        for obj in objects_list:
            if counter == 500:
                batch.commit()
                print('Written {} objects into "{}"'.format(counter, collection))
                counter = 0

            doc_id = obj.get('id')
            if doc_id is None:
                continue
            ref = db.collection(collection).document(doc_id)
            batch.set(ref, obj, merge=merge)
            counter += 1

        batch.commit()
        print('Written {} objects into "{}"'.format(len(objects_list), collection))

    @classmethod
    def _remove_list(cls, objects_id_list: list, merge: bool = False):
        """
        Batch save the list of object into collection_to_listen
        tries to save with chunks of 500 items

        :param objects_list: list of objects of type object, each must have an id field
        :param merge: should the object be merged with that is already exists in the database
        """
        collection = cls.name
        if not collection or not isinstance(objects_id_list, list):
            return
        batch = db.batch()
        counter = 0
        for obj_id in objects_id_list:
            if counter == 500:
                batch.commit()
                print('Deleted {} objects into "{}"'.format(counter, collection))
                counter = 0

            ref = db.collection(collection).document(obj_id)
            batch.delete(ref)
            counter += 1

        batch.commit()
        print('Deleted {} objects into "{}"'.format(len(objects_id_list), collection))

    @classmethod
    def _save(cls,
              obj: object,
              doc_id: str = None,
              merge: bool = False
              ):
        """
        Saves an object into collection_to_listen

        :param doc_id:
        :param obj: object to save
        :param merge: should the object be merged with that is already exists in the database
        """
        collection = cls.name
        print(obj)
        if not collection or not isinstance(obj, object):
            return
        ref = db.collection(collection)
        if doc_id:
            ref = ref.document(doc_id)
        else:
            ref = ref.document()
        result = ref.set(obj, merge=merge)
        return result

    @classmethod
    def _get_all(cls, limit: int = None):
        ref = db.collection(cls.name)
        if limit:
            ref.limit(limit)
        docs = ref.stream()
        return [doc.to_dict() for doc in docs]

    @classmethod
    def _get_doc(cls, doc_id):
        ref = db.collection(cls.name).document(doc_id)
        doc = ref.get().to_dict()
        return doc

    @classmethod
    def doc_ref_with_id(cls, doc_id) -> DocumentReference:
        ref = db.collection(cls.name).document(doc_id)
        return ref