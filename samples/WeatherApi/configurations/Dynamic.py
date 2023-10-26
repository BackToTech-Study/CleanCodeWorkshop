import json


class Dynamic:
    @classmethod
    def fromDict(cls, dict):
        obj = cls()
        obj.__dict__.update(dict)
        return obj

    @classmethod
    def fromJson(cls, jsonString: str):
        if not jsonString:
            return None
        return json.loads(jsonString, object_hook=cls.fromDict)

    @classmethod
    def fromFile(cls, source):
        rawData = None
        with open(source) as inputStream:
            rawData = inputStream.read()
        return cls.fromJson(rawData)
