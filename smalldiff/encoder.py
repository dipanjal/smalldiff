import json
from datetime import datetime, date
from enum import Enum
from json import JSONEncoder


class ModelEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, Enum):
                return obj.value
            if isinstance(obj, (date, datetime)):
                return obj.isoformat()
            if isinstance(obj, (bytes, bytearray)):
                return obj.decode('utf-8')
            if isinstance(obj, (set, frozenset)):
                return list(obj)
            if isinstance(obj, object):
                if hasattr(obj, 'to_dict'):
                    return obj.to_dict()
                if hasattr(obj, '__dict__'):
                    return obj.__dict__
            return json.JSONEncoder.default(self, obj)
        except TypeError as e:
            msg = (f'{e}, provide a customer encoder by extending ModelEncoder '
                   f'or implement to_dict() method')
            raise TypeError(msg) from e
