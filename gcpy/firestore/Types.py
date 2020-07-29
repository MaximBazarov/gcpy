import google.cloud.firestore_v1.document as firestore_document
from google.api_core.datetime_helpers import DatetimeWithNanoseconds


class FirestoreType:
    """
        Firestore type definition
    """

    def __init__(self):
        self.value = None

    @staticmethod
    def map_change(changes: dict):
        """
        Initialising the new instance with a `Value`_ dictionary

        Args:
            changes (dict): The value represented by a `Value`

        .. _Value:
            https://cloud.google.com/firestore/docs/reference/rest/v1/Value

        """
        pass

    #
    # def __init__(self,
    #              doc: firestore_document.DocumentReference):
    #     """
    #     Initialising the new instance with a `DocumentReference`_ object
    #
    #     Args:
    #         doc (DocumentReference): a `DocumentReference`
    #
    #     .. _DocumentReference:
    #         https://googleapis.dev/python/firestore/latest/document.html
    #
    #     """
    #
    #     self.x = x


class String(FirestoreType):

    def __init__(self, string: str):
        self.value = string

    @staticmethod
    def map_change(changes: dict):
        if changes is None or not isinstance(changes, dict):
            raise ValueError("Changes for string value must be a dict containing a stringValue key")

        return String(changes.get('stringValue'))


class Number(FirestoreType):
    def __init__(self, number: float):
        self.value = number

    @staticmethod
    def map_change(changes: dict):
        if changes is None or not isinstance(changes, dict):
            raise ValueError("Changes for Number value must be a dict containing a integerValue or a doubleValue key")
        integer_value = changes.get('integerValue')
        if integer_value is not None:
            return Number(float(int(integer_value)))
        return Number(changes.get('doubleValue'))


class DateTime(FirestoreType):

    def __init__(self, timestamp: str):
        self.value = DatetimeWithNanoseconds.from_rfc3339(timestamp)

    @staticmethod
    def map_change(changes: dict):
        if changes is None or not isinstance(changes, dict):
            raise ValueError("changes must be dict")
        timestamp = changes.get('timestampValue')
        if not timestamp:
            return None

        return DateTime(timestamp)


class Integer(FirestoreType):
    def __init__(self, value: int):
        self.value = value

    @staticmethod
    def map_change(changes: dict):
        if changes is None or not isinstance(changes, dict):
            raise ValueError("Changes for Integer value must be a dict containing a integerValue ")
        integer_value = int(changes.get('integerValue', ''))
        if not isinstance(integer_value, int):
            return None
        return Integer(value=integer_value)


class Boolean(FirestoreType):

    def __init__(self, value: bool):
        self.value = value

    @staticmethod
    def map_change(changes: dict):
        if changes is None or not isinstance(changes, dict):
            raise ValueError("Changes for Boolean value must be a dict containing a booleanValue key")

        return Boolean(changes.get('booleanValue'))
