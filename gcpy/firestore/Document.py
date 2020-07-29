from gcpy.firestore import Types
import google.cloud.firestore_v1.document as firestore_document

from gcpy.firestore.Types import FirestoreType


class Changes:
    def __init__(self, old, new):
        self.old = old
        self.new = new


class Document:
    """
    Document represents the Firestore document.

    fields is a map of field names to their types e.g.
    Example:
            'id': FirestoreTypes.String

    Required:
     * to also have **__init__** that contains all this fields with the same names
    to be able to initialise them with values,
     * to have default values in the **__init__** to be able to initialise without parameters

    """
    fields = {
        'id': Types.String,
    }

    def __init__(self, id: str = None):
        self.id = id

    @classmethod
    def map_changes(cls, change):
        """
        Maps changes
        Args:
            change:

        Returns:

        """

        if change is None:
            return None
        fields = cls.fields
        new = cls()
        if not change:
            return new
        for field in fields:
            changed_field = change.get(field)
            if changed_field:
                mapped_change = fields[field].map_change(changed_field)
                if isinstance(mapped_change, FirestoreType):
                    new.__setattr__(field, mapped_change.value)
        return new

    @classmethod
    def changes(cls, changes: dict):
        return Changes(
            old=cls.map_changes(changes.get('oldValue', {}).get('fields')),
            new=cls.map_changes(changes.get('value', {}).get('fields'))
        )

    @classmethod
    def from_snapshot(cls, doc: firestore_document.DocumentSnapshot):
        data = doc.to_dict()
        return cls.from_dict(data)

    @classmethod
    def from_dict(cls, data: dict):
        result = cls()
        if not data:
            return result
        for key in data:
            if key in cls.fields:
                result.__setattr__(key, data[key])
            else:
                print('[WARNING]: {}.from_snapshot(): field {} is not in the {} fields'
                      .format(cls.__name__, key, cls.__name__))
        return result

    def diff_fields(self, document):
        changed_fields = set([])
        self_attributes = set(vars(self))
        if document is None:
            return self_attributes
        new_attributes = set(vars(document))
        all_attributes = {*self_attributes, *new_attributes}
        for field in all_attributes:
            if field not in new_attributes:
                continue

            if field not in self_attributes and field in new_attributes:
                changed_fields.add(field)
                continue

            current_value = self.__getattribute__(field)
            new_value = document.__getattribute__(field)
            if current_value != new_value:
                changed_fields.add(field)
        return changed_fields

    def __iter__(self):
        attributes = vars(self)
        for name in attributes:
            if attributes[name] is not None:  # skip None fields
                yield name, attributes[name]
