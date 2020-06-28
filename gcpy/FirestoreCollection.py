from datetime import datetime
from enum import Enum

from google.cloud import firestore

db = firestore.Client()


class FirestoreTypeDefinition:
    def __init__(self, python_type: type, firestore_type_names: list):
        self.python_type = python_type
        self.firestore_type_names = firestore_type_names


class FirestoreFieldType(Enum):

    @staticmethod
    def number() -> FirestoreTypeDefinition:
        return FirestoreTypeDefinition(
            python_type=float,
            firestore_type_names=[
                'integerValue',
                'doubleValue'
            ]
        )

    @staticmethod
    def string(self):
        return FirestoreTypeDefinition(
            python_type=str,
            firestore_type_names=[
                'stringValue'
            ]
        )

    @staticmethod
    def datetime(self):
        return FirestoreTypeDefinition(
            python_type=datetime,
            firestore_type_names=[
                'datetimeValue'
            ]
        )

    @staticmethod
    def map(self):
        return FirestoreTypeDefinition(
            python_type=datetime,
            firestore_type_names=[
                'mapValue'
            ]
        )

    @staticmethod
    def array(self):
        return FirestoreTypeDefinition(
            python_type=datetime,
            firestore_type_names=[
                'arrayValue'
            ]
        )


class FirestoreDocumentField:
    def __init__(
            self,
            name: str,
            field_type: FirestoreTypeDefinition
    ):
        """

        Creates a FirestoreDocumentField

        :param name: name of the field
        :param field_type: FirestoreFieldType type function e.g. FirestoreFieldType.number
        """
        self.name = name
        self.field_type = field_type


class FirestoreDocument:
    fields = []


class Changes:
    def __init__(self, old, new):
        self.old = old
        self.new = new


class FirestoreCollection:
    # Collection name
    name = ''
    document_type = FirestoreDocument

    asc = 'ASCENDING'
    desc = 'DESCENDING'

    def _save_list(self, objects_list: list, merge: bool = False):
        """
        Batch save the list of object into collection_to_listen
        tries to save with chunks of 500 items

        :param objects_list: list of objects of type object, each must have an id field
        :param merge: should the object be merged with that is already exists in the database
        """
        collection = self.name
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

    def _remove_list(self, objects_id_list: list, merge: bool = False):
        """
        Batch save the list of object into collection_to_listen
        tries to save with chunks of 500 items

        :param objects_list: list of objects of type object, each must have an id field
        :param merge: should the object be merged with that is already exists in the database
        """
        collection = self.name
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

    def _save(self,
              obj: object,
              doc_id: str,
              merge: bool = False
              ):
        """
        Saves an object into collection_to_listen

        :param doc_id:
        :param obj: object to save
        :param merge: should the object be merged with that is already exists in the database
        """
        collection = self.name
        print(obj)
        if not collection or not isinstance(obj, object):
            return
        ref = db.collection(collection).document(doc_id)
        result = ref.set(obj, merge=merge)
        return result

    def _get_all(self, limit: int = None):
        ref = db.collection(self.name)
        if limit:
            ref.limit(limit)
        docs = ref.stream()
        return [doc.to_dict() for doc in docs]

    def _get_doc(self, doc_id):
        ref = db.collection(self.name).document(doc_id)
        doc = ref.get().to_dict()
        return doc

    #
    # HANDLING UPDATES

    def map_fields(self, fields: dict):
        """
        To override in ancestors

        :param fields:
        :return:
        """
        return None

    def changes_from_event(self, event):
        old_data = event.get('oldValue', {}).get('fields', {})
        new_data = event.get('value', {}).get('fields', {})
        return Changes(
            old=self.map_fields(old_data),
            new=self.map_fields(new_data)
        )
