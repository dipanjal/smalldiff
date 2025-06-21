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

    # Additional test cases for better coverage

    def test_encode_frozenset(self):
        """Test encoding frozenset objects specifically."""
        data = {'frozenset': frozenset([1, 2, 3])}
        expected = '{"frozenset": [1, 2, 3]}'
        actual = json.dumps(data, cls=ModelEncoder)
        self.assertEqual(actual, expected)

    def test_encode_bytearray(self):
        """Test encoding bytearray objects specifically."""
        data = {'bytearray': bytearray(b'hello world')}
        expected = '{"bytearray": "hello world"}'
        actual = json.dumps(data, cls=ModelEncoder)
        self.assertEqual(actual, expected)

    def test_encode_empty_containers(self):
        """Test encoding empty containers."""
        data = {
            'empty_set': set(),
            'empty_frozenset': frozenset(),
            'empty_bytes': b'',
            'empty_bytearray': bytearray()
        }
        expected = '{"empty_set": [], "empty_frozenset": [], "empty_bytes": "", "empty_bytearray": ""}'
        actual = json.dumps(data, cls=ModelEncoder)
        self.assertEqual(actual, expected)

    def test_encode_object_with_both_dict_and_to_dict(self):
        """Test that to_dict() takes priority over __dict__."""
        class TestObject:
            def __init__(self):
                self.attr1 = "value1"
                self.attr2 = "value2"
            
            def to_dict(self):
                return {"custom": "method", "priority": True}
        
        data = {'obj': TestObject()}
        expected = '{"obj": {"custom": "method", "priority": true}}'
        actual = json.dumps(data, cls=ModelEncoder)
        self.assertEqual(actual, expected)

    def test_encode_object_with_only_dict(self):
        """Test object with only __dict__ attribute."""
        class SimpleObject:
            def __init__(self):
                self.name = "test"
                self.value = 42
        
        data = {'obj': SimpleObject()}
        expected = '{"obj": {"name": "test", "value": 42}}'
        actual = json.dumps(data, cls=ModelEncoder)
        self.assertEqual(actual, expected)

    def test_encode_object_without_dict_or_to_dict(self):
        """Test object without __dict__ or to_dict method."""
        class SlotsObject:
            __slots__ = ['name', 'value']
            
            def __init__(self):
                self.name = "test"
                self.value = 42
        
        data = {'obj': SlotsObject()}
        # This should fall back to JSONEncoder.default which will raise TypeError
        with self.assertRaises(TypeError):
            json.dumps(data, cls=ModelEncoder)

    def test_encode_none_value(self):
        """Test encoding None values."""
        data = {'none_value': None}
        expected = '{"none_value": null}'
        actual = json.dumps(data, cls=ModelEncoder)
        self.assertEqual(actual, expected)

    def test_encode_nested_structures(self):
        """Test encoding nested structures with custom objects."""
        class NestedObject:
            def __init__(self, name):
                self.name = name
            
            def to_dict(self):
                return {"name": self.name, "type": "nested"}
        
        data = {
            'nested': {
                'list': [1, 2, NestedObject("test")],
                'set': {1, 2, 3},
                'bytes': b'nested bytes'
            }
        }
        expected = '{"nested": {"list": [1, 2, {"name": "test", "type": "nested"}], "set": [1, 2, 3], "bytes": "nested bytes"}}'
        actual = json.dumps(data, cls=ModelEncoder)
        self.assertEqual(actual, expected)

    def test_encode_complex_enum(self):
        """Test encoding enum with string values."""
        class Status(Enum):
            PENDING = "pending"
            ACTIVE = "active"
            INACTIVE = "inactive"
        
        data = {'status': Status.ACTIVE}
        expected = '{"status": "active"}'
        actual = json.dumps(data, cls=ModelEncoder)
        self.assertEqual(actual, expected)

    def test_encode_multiple_enums(self):
        """Test encoding multiple enum values."""
        class Direction(Enum):
            NORTH = "north"
            SOUTH = "south"
            EAST = "east"
            WEST = "west"
        
        data = {
            'directions': [Direction.NORTH, Direction.SOUTH],
            'current': Direction.EAST
        }
        expected = '{"directions": ["north", "south"], "current": "east"}'
        actual = json.dumps(data, cls=ModelEncoder)
        self.assertEqual(actual, expected)

    def test_encode_datetime_with_timezone(self):
        """Test encoding datetime with timezone info."""
        from datetime import timezone
        
        dt = datetime(2023, 4, 8, 12, 34, 56, tzinfo=timezone.utc)
        data = {'datetime': dt}
        expected = '{"datetime": "2023-04-08T12:34:56+00:00"}'
        actual = json.dumps(data, cls=ModelEncoder)
        self.assertEqual(actual, expected)

    def test_encode_bytes_with_special_characters(self):
        """Test encoding bytes with special characters."""
        data = {'bytes': b'hello\x00world\n\t\r'}
        expected = '{"bytes": "hello\\u0000world\\n\\t\\r"}'
        actual = json.dumps(data, cls=ModelEncoder)
        self.assertEqual(actual, expected)

    def test_encode_set_with_mixed_types(self):
        """Test encoding set with mixed types."""
        data = {"mixed_set": {True, None, 10, "string"}}
        # Note: JSON doesn't support None in sets, but our encoder converts to list
        expected = '{"mixed_set": [null, 10, true, "string"]}'
        actual = json.dumps(data, cls=ModelEncoder)
        # Sort both lists for comparison since set order is not guaranteed
        actual_dict = json.loads(actual)
        expected_dict = json.loads(expected)
        self.assertEqual(
            sorted(actual_dict['mixed_set'], key=str),
            sorted(expected_dict['mixed_set'], key=str)
        )

    def test_encode_set_with_boolean_integer_overlap(self):
        """Test that True and 1 are treated as equal in Python sets."""
        # This demonstrates a Python set limitation, not an encoder issue
        data = {"mixed_set": {True, 1, False, 0}}
        # In Python: True == 1 and False == 0, so the set becomes {True, False}
        expected = '{"mixed_set": [false, true]}'
        actual = json.dumps(data, cls=ModelEncoder)
        # Sort both lists for comparison since set order is not guaranteed
        actual_dict = json.loads(actual)
        expected_dict = json.loads(expected)
        self.assertEqual(
            sorted(actual_dict['mixed_set']),
            sorted(expected_dict['mixed_set'])
        )

    def test_encode_set_with_distinct_integers_and_booleans(self):
        """Test encoding set with distinct integers and booleans."""
        data = {"mixed_set": {True, False, 2, 3, "string"}}
        expected = '{"mixed_set": [false, 2, 3, true, "string"]}'
        actual = json.dumps(data, cls=ModelEncoder)
        # Sort both lists for comparison since set order is not guaranteed
        actual_dict = json.loads(actual)
        expected_dict = json.loads(expected)
        self.assertEqual(sorted(actual_dict['mixed_set'], key=str), sorted(expected_dict['mixed_set'], key=str))

    def test_encode_object_with_complex_attributes(self):
        """Test encoding object with complex attributes."""
        class ComplexObject:
            def __init__(self):
                self.string_attr = "hello"
                self.int_attr = 42
                self.float_attr = 3.14
                self.bool_attr = True
                self.none_attr = None
                self.list_attr = [1, 2, 3]
                self.dict_attr = {"key": "value"}
        
        data = {'complex': ComplexObject()}
        expected = '{"complex": {"string_attr": "hello", "int_attr": 42, "float_attr": 3.14, "bool_attr": true, "none_attr": null, "list_attr": [1, 2, 3], "dict_attr": {"key": "value"}}}'
        actual = json.dumps(data, cls=ModelEncoder)
        self.assertEqual(actual, expected)

    def test_encode_error_handling(self):
        """Test that TypeError is properly raised with custom message."""
        # Use a built-in object that can't be serialized by JSON
        import sys
        data = {'obj': sys.modules}  # sys.modules is a dict-like object that can't be serialized
        
        with self.assertRaises(TypeError) as context:
            json.dumps(data, cls=ModelEncoder)
        
        self.assertIn("provide a customer encoder by extending ModelEncoder", str(context.exception))

    def test_encode_error_handling_with_slots_object(self):
        """Test that TypeError is properly raised for objects without __dict__ or to_dict."""
        class SlotsObject:
            __slots__ = ['name', 'value']
            
            def __init__(self):
                self.name = "test"
                self.value = 42
        
        data = {'obj': SlotsObject()}
        
        with self.assertRaises(TypeError) as context:
            json.dumps(data, cls=ModelEncoder)
        
        self.assertIn("provide a customer encoder by extending ModelEncoder", str(context.exception))

    def test_encode_custom_encoder_extension(self):
        """Test extending ModelEncoder with custom functionality."""
        class CustomEncoder(ModelEncoder):
            def default(self, obj):
                if hasattr(obj, 'custom_serialize'):
                    return obj.custom_serialize()
                return super().default(obj)
        
        class CustomObject:
            def __init__(self, value):
                self.value = value
            
            def custom_serialize(self):
                return f"CUSTOM_{self.value}"
        
        data = {'custom': CustomObject("test")}
        expected = '{"custom": "CUSTOM_test"}'
        actual = json.dumps(data, cls=CustomEncoder)
        self.assertEqual(actual, expected)

    def test_encode_custom_encoder_with_standard_types(self):
        """Test that custom encoder still handles standard types."""
        class CustomEncoder(ModelEncoder):
            def default(self, obj):
                if hasattr(obj, 'custom_serialize'):
                    return obj.custom_serialize()
                return super().default(obj)
        
        class CustomObject:
            def __init__(self, value):
                self.value = value
            
            def custom_serialize(self):
                return f"CUSTOM_{self.value}"
        
        class TestEnum(Enum):
            VALUE1 = 1
            VALUE2 = 2
        
        data = {
            'custom': CustomObject("test"),
            'enum': TestEnum.VALUE1,
            'set': {1, 2, 3},
            'bytes': b'hello'
        }
        expected = '{"custom": "CUSTOM_test", "enum": 1, "set": [1, 2, 3], "bytes": "hello"}'
        actual = json.dumps(data, cls=CustomEncoder)
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
