import unittest
import json
from datetime import datetime, date
from enum import Enum

from smalldiff.encoder import ModelEncoder


class TestModelEncoder(unittest.TestCase):

    def test_encode_enum(self):
        class Color(Enum):
            RED = 1
            GREEN = 2
            BLUE = 3

        data = {'color': Color.RED}
        expected = '{"color": 1}'
        actual = json.dumps(data, cls=ModelEncoder)
        self.assertEqual(actual, expected)

    def test_encode_date(self):
        data = {'date': date(2023, 4, 8)}
        expected = '{"date": "2023-04-08"}'

        # Suppose, the default ModelEncoder has no functionality to convert date object
        # You can simply provide your customer JSONEncoder by extending the default ModelEncoder
        class DateEncoder(ModelEncoder):
            def default(self, obj):
                if isinstance(obj, date):
                    return obj.isoformat()
                return ModelEncoder.default(self, obj)

        actual = json.dumps(data, cls=DateEncoder)
        self.assertEqual(actual, expected)

    def test_encode_datetime(self):
        data = {'datetime': datetime(2023, 4, 8, 12, 34, 56)}
        expected = '{"datetime": "2023-04-08T12:34:56"}'
        # Overriding default method's behaviour but this is not supported for smalldiff compare method
        # Because in smalldiff we already have a ModelEncoder with bunch of known type converters
        # But if you override the default method explicitly, you won't get the other type converters support
        actual = json.dumps(
            obj=data,
            default=lambda o: o.isoformat() if isinstance(o, datetime) else None
        )
        self.assertEqual(actual, expected)

    def test_encode_bytes(self):
        data = {'bytes': b'hello world'}
        expected = '{"bytes": "hello world"}'
        actual = json.dumps(data, cls=ModelEncoder)
        self.assertEqual(actual, expected)

    def test_encode_set(self):
        data = {'set': {1, 2, 3}}
        expected = '{"set": [1, 2, 3]}'
        actual = json.dumps(data, cls=ModelEncoder)
        self.assertEqual(actual, expected)

    def test_encode_tuple(self):
        data = {'tuple': (1, 'two', {'three': 3})}
        expected = '{"tuple": [1, "two", {"three": 3}]}'
        actual = json.dumps(data, cls=ModelEncoder)
        self.assertEqual(actual, expected)

    def test_encode_list(self):
        data = {'list': [1, 'two', {'three': 3}]}
        expected = '{"list": [1, "two", {"three": 3}]}'
        actual = json.dumps(data, cls=ModelEncoder)
        self.assertEqual(actual, expected)

    def test_encode_object_with_dict(self):
        class Person:
            def __init__(self, name, age):
                self.name = name
                self.age = age

            def to_dict(self):
                return {'name': self.name, 'age': self.age}

        data = {'person': Person('John', 30)}
        expected = '{"person": {"name": "John", "age": 30}}'
        actual = json.dumps(data, cls=ModelEncoder)
        self.assertEqual(actual, expected)

    def test_encode_object_without_dict(self):
        class Car:
            def __init__(self, make, model, year):
                self.make = make
                self.model = model
                self.year = year

        data = {'car': Car('Ford', 'Mustang', 2022)}
        expected = '{"car": {"make": "Ford", "model": "Mustang", "year": 2022}}'
        actual = json.dumps(data, cls=ModelEncoder)
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
