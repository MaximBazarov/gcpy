import json


class BinaryPayload:
    """
    Binary payload to use in HTTP handlers.
    Subclasses __init__ **must** have default values for all the parameters
    to be able to instantiate via calling `cls()`

    """

    @classmethod
    def by_decoding(cls, binary_payload: bytes):
        """
        Decodes bytes and returns the instance of the BinaryPayload or its subclass.

        Args:
            binary_payload:

        Returns: the instance of the BinaryPayload or subclass using bytes

        """
        data = json.loads(binary_payload.decode("UTF-8"))
        result = cls()
        attributes = vars(result)
        if not data:
            return result
        for key in data:
            if key in attributes:
                result.__setattr__(key, data[key])
            else:
                print('[WARNING]: {}.from_snapshot(): field {} is not in the {} fields'
                      .format(cls.__name__, key, cls.__name__))
        return result

    def encode(self) -> bytes:
        """
        Returns: BinaryPayload encoded to bytes
        """

        payload = dict(self)
        return json.dumps(payload).encode()

    def __iter__(self):
        attributes = vars(self)
        for name in attributes:
            if attributes[name] is not None:  # skip None fields
                yield name, attributes[name]
