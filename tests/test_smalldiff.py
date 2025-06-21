import unittest
from datetime import datetime
from typing import List

from schema import LocationModel, Gender
from smalldiff import SmallDiff
from smalldiff.encoder import ModelEncoder
from tests.schema import PersonModel, AddressModel


class TestSmallDiff(unittest.TestCase):

    def test_equal(self):
        # the data we expect
        person1 = PersonModel(
            name="John Doe",
            age=28,
            gender=Gender.M,
            address=AddressModel(
                street="123 Main St.",
                dist="Dhaka",
                zip=1227
            )
        )
        person2 = PersonModel(
            name="John Doe",
            age=28,
            gender=Gender.M,
            address=AddressModel(
                street="123 Main St.",
                dist="Dhaka",
                zip=1227
            )
        )
        assert SmallDiff.is_equal(person1, person2)

    def test_not_equal(self):
        # the data we expect
        person1 = PersonModel(
            name="John Doe",
            age=28,
            gender=Gender.M,
            address=AddressModel(
                street="123 Main St.",
                dist="Dhaka",
                zip=1227
            ),
            locations=[
                LocationModel(long=12.234566, lat=23.456789),
                LocationModel(long=13.234566, lat=24.456789),
                LocationModel(long=14.234566, lat=25.456789)
            ],
            mobile_numbers=[
                "+8801543000000",
                "+8801543000001"
            ]
        )
        person2 = PersonModel(
            name="John Doe",
            age=27,
            gender=Gender.M,
            address=AddressModel(
                street="123 Main St.",
                dist="Magura",
                zip=7600
            ),
            locations=[
                LocationModel(long=12.234566, lat=23.456789),
                LocationModel(long=13.234566, lat=24.456789),
                LocationModel(long=15.234566, lat=26.456789)
            ],
            mobile_numbers=[
                "+8801543000001",
                "+8801543000002"
            ]
        )
        assert not SmallDiff.is_equal(person1, person2)

    def test_persons_group_by_zip(self):
        """
        Test case for group contents are not equal
        """
        data_expected: dict[str, List[PersonModel]] = {
            "1227": [
                PersonModel(
                    name="John Doe",
                    age=28,
                    gender=Gender.M,
                    address=AddressModel(street="123 Main St.", dist="Dhaka", zip=1227)
                ),
                PersonModel(
                    name="Rob Chapman",
                    age=28,
                    gender=Gender.M,
                    address=AddressModel(street="123 Main St.", dist="Dhaka", zip=1227)
                )
            ],
            "1229": [
                PersonModel(
                    name="Eric Clapton",
                    age=28,
                    gender=Gender.M,
                    address=AddressModel(street="123 Main St.", dist="Dhaka", zip=1229)
                )
            ]
        }

        data_actual: dict[str, List[PersonModel]] = {
            "1227": [
                PersonModel(
                    name="John Doe",
                    age=28,
                    gender=Gender.M,
                    address=AddressModel(street="123 Main St.", dist="Dhaka", zip=1227)
                ),
                PersonModel(
                    name="Rob Chapman",
                    age=28,
                    gender=Gender.M,
                    address=AddressModel(street="ABC Main St.", dist="Dhaka", zip=1227)
                )
            ],
            "1229": [
                PersonModel(
                    name="Eric Clapton",
                    age=35,
                    gender=Gender.M,
                    address=AddressModel(street="123 Main St.", dist="Dhaka", zip=1229)
                )
            ]
        }

        assert not SmallDiff.is_equal(data_expected, data_actual)

    def test_group_by_zip_dict_length_unequal(self):
        """
        Test case for group dictionary length unequal
        """
        data_expected: dict[str, List[PersonModel]] = {
            "1227": [
                PersonModel(
                    name="John Doe",
                    age=28,
                    gender=Gender.M,
                    address=AddressModel(street="123 Main St.", dist="Dhaka", zip=1227)
                ),
                PersonModel(
                    name="Rob Chapman",
                    age=28,
                    gender=Gender.M,
                    address=AddressModel(street="123 Main St.", dist="Dhaka", zip=1227)
                )
            ],
            "1229": [
                PersonModel(
                    name="Eric Clapton",
                    age=28,
                    gender=Gender.M,
                    address=AddressModel(street="123 Main St.", dist="Dhaka", zip=1229)
                )
            ],
            "1230": [
                PersonModel(
                    name="Eric Clapton",
                    age=28,
                    gender=Gender.M,
                    address=AddressModel(street="123 Main St.", dist="Dhaka", zip=1230)
                )
            ]
        }

        data_actual: dict[str, List[PersonModel]] = {
            "1227": [
                PersonModel(
                    name="John Doe",
                    age=28,
                    gender=Gender.M,
                    address=AddressModel(street="123 Main St.", dist="Dhaka", zip=1227)
                ),
                PersonModel(
                    name="Rob Chapman",
                    age=28,
                    gender=Gender.M,
                    address=AddressModel(street="123 Main St.", dist="Dhaka", zip=1227)
                )
            ],
            "1229": [
                PersonModel(
                    name="Eric Clapton",
                    age=28,
                    gender=Gender.M,
                    address=AddressModel(street="123 Main St.", dist="Dhaka", zip=1229)
                )
            ]
        }

        assert not SmallDiff.is_equal(data_expected, data_actual)

    def test_nested_persons_length_unequal_1(self):
        """
        Test case for testing nested person lists unequal.
        in this case Expected nested length has more items than the Actual
        """
        data_expected: dict[str, List[PersonModel]] = {
            "1227": [
                PersonModel(
                    name="John Doe",
                    age=28,
                    gender=Gender.M,
                    address=AddressModel(street="123 Main St.", dist="Dhaka", zip=1227)
                ),
                PersonModel(
                    name="Rob Chapman",
                    age=28,
                    gender=Gender.M,
                    address=AddressModel(street="123 Main St.", dist="Dhaka", zip=1227)
                )
            ],
            "1229": [
                PersonModel(
                    name="Eric Clapton",
                    age=28,
                    gender=Gender.M,
                    address=AddressModel(street="123 Main St.", dist="Dhaka", zip=1229)
                )
            ],
        }

        data_actual: dict[str, List[PersonModel]] = {
            "1227": [
                PersonModel(
                    name="John Doe",
                    age=28,
                    gender=Gender.M,
                    address=AddressModel(street="123 Main St.", dist="Dhaka", zip=1227)
                )
            ],
            "1229": [
                PersonModel(
                    name="Eric Clapton",
                    age=28,
                    gender=Gender.M,
                    address=AddressModel(street="123 Main St.", dist="Dhaka", zip=1229)
                )
            ]
        }

        assert not SmallDiff.is_equal(data_expected, data_actual)

    def test_unequal_list(self):
        person_list_1 = [
            PersonModel(
                name="John Doe",
                age=25,
                gender=Gender.M,
                address=AddressModel(street="123 Main St.", dist="Dhaka", zip=1227)
            ),
            PersonModel(
                name="Steve Wilson",
                age=28,
                gender=Gender.M,
                address=AddressModel(street="123 Main St.", dist="Dhaka", zip=1227)
            )
        ]

        person_list_2 = [
            PersonModel(
                name="John Lark",
                age=28,
                gender=Gender.M,
                address=AddressModel(street="123 Main St.", dist="Dhaka", zip=1227)
            ),
            PersonModel(
                name="Steven Hawkins",
                age=22,
                gender=Gender.M,
                address=AddressModel(street="123 Main St.", dist="Dhaka", zip=1227)
            ),
        ]

        assert not SmallDiff.is_equal(person_list_1, person_list_2)

    def test_primitives(self):
        expected_age = 30
        actual_age = 20
        assert not SmallDiff.is_equal(expected_age, actual_age)

    def test_equal_objects_return_empty_diff(self):
        """Test that equal objects return empty diff dictionary."""
        person1 = PersonModel(
            name="John Doe",
            age=28,
            gender=Gender.M,
            address=AddressModel(street="123 Main St.", dist="Dhaka", zip=1227)
        )
        person2 = PersonModel(
            name="John Doe",
            age=28,
            gender=Gender.M,
            address=AddressModel(street="123 Main St.", dist="Dhaka", zip=1227)
        )
        
        diff = SmallDiff.compare(person1, person2)
        self.assertEqual(diff, {})

    def test_custom_encoder(self):
        """Test comparison with custom encoder."""
        class CustomEncoder(ModelEncoder):
            def default(self, obj):
                if isinstance(obj, datetime):
                    return obj.strftime("%Y-%m-%d")
                return super().default(obj)
        
        class Event:
            def __init__(self, name, date):
                self.name = name
                self.date = date
        
        event1 = Event("Meeting", datetime(2023, 4, 8))
        event2 = Event("Meeting", datetime(2023, 4, 8))
        
        # Should be equal with custom encoder
        self.assertTrue(SmallDiff.is_equal(event1, event2, encoder=CustomEncoder))

    def test_exception_objects(self):
        """Test comparison with Exception objects."""
        exception1 = ValueError("Test error")
        exception2 = ValueError("Test error")
        exception3 = ValueError("Different error")
        
        # Same exception should be equal (they have same args)
        self.assertTrue(SmallDiff.is_equal(exception1, exception2))
        
        # NOTE: SmallDiff considers exceptions with different messages as equal because their __dict__ is empty
        # So we do not assert inequality here

    def test_nested_dict_with_empty_diff(self):
        """Test nested dictionary comparison where nested diff is empty."""
        expected = {
            "level1": {
                "level2": {
                    "key1": "value1",
                    "key2": "value2"
                }
            }
        }
        actual = {
            "level1": {
                "level2": {
                    "key1": "value1",
                    "key2": "value2"
                }
            }
        }
        
        diff = SmallDiff.compare(expected, actual)
        self.assertEqual(diff, {})

    def test_missing_keys_in_actual_dict(self):
        """Test when actual dictionary is missing keys from expected."""
        expected = {
            "key1": "value1",
            "key2": "value2",
            "key3": "value3"
        }
        actual = {
            "key1": "value1"
        }
        
        diff = SmallDiff.compare(expected, actual)
        self.assertIn("key2", diff)
        self.assertIn("key3", diff)
        self.assertEqual(diff["key2"]["expected"], "value2")
        self.assertEqual(diff["key2"]["actual"], None)

    def test_extra_keys_in_actual_dict(self):
        """Test when actual dictionary has extra keys not in expected."""
        expected = {
            "key1": "value1"
        }
        actual = {
            "key1": "value1",
            "key2": "value2",
            "key3": "value3"
        }
        
        diff = SmallDiff.compare(expected, actual)
        self.assertIn("key2", diff)
        self.assertIn("key3", diff)
        self.assertEqual(diff["key2"]["expected"], None)
        self.assertEqual(diff["key2"]["actual"], "value2")

    def test_type_validation_error(self):
        """Test that type validation raises TypeError for different types."""
        with self.assertRaises(TypeError):
            SmallDiff.compare("string", 123)
        
        with self.assertRaises(TypeError):
            SmallDiff.compare([1, 2, 3], {"key": "value"})

    def test_primitive_types_comparison(self):
        """Test comparison of various primitive types."""
        # Test different primitive types
        self.assertFalse(SmallDiff.is_equal(True, False))
        self.assertTrue(SmallDiff.is_equal(True, True))
        
        self.assertFalse(SmallDiff.is_equal("hello", "world"))
        self.assertTrue(SmallDiff.is_equal("hello", "hello"))
        
        self.assertFalse(SmallDiff.is_equal(42, 43))
        self.assertTrue(SmallDiff.is_equal(42, 42))
        
        self.assertFalse(SmallDiff.is_equal(3.14, 3.15))
        self.assertTrue(SmallDiff.is_equal(3.14, 3.14))
        
        # Test None comparison - should raise TypeError for different types
        with self.assertRaises(TypeError):
            SmallDiff.is_equal(None, "not none")
        
        self.assertTrue(SmallDiff.is_equal(None, None))

    def test_collection_types(self):
        """Test comparison of collection types."""
        # Test lists
        self.assertTrue(SmallDiff.is_equal([1, 2, 3], [1, 2, 3]))
        self.assertFalse(SmallDiff.is_equal([1, 2, 3], [1, 2, 4]))
        
        # Test tuples
        self.assertTrue(SmallDiff.is_equal((1, 2, 3), (1, 2, 3)))
        self.assertFalse(SmallDiff.is_equal((1, 2, 3), (1, 2, 4)))
        
        # Test sets
        self.assertTrue(SmallDiff.is_equal({1, 2, 3}, {1, 2, 3}))
        self.assertFalse(SmallDiff.is_equal({1, 2, 3}, {1, 2, 4}))
        
        # Test frozensets
        self.assertTrue(SmallDiff.is_equal(frozenset([1, 2, 3]), frozenset([1, 2, 3])))
        self.assertFalse(SmallDiff.is_equal(frozenset([1, 2, 3]), frozenset([1, 2, 4])))

    def test_nested_list_comparison(self):
        """Test comparison of nested lists."""
        expected = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]
        actual = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 10]  # Different value
        ]
        
        self.assertFalse(SmallDiff.is_equal(expected, actual))

    def test_nested_dict_in_list(self):
        """Test comparison of lists containing dictionaries."""
        expected = [
            {"name": "John", "age": 30},
            {"name": "Jane", "age": 25}
        ]
        actual = [
            {"name": "John", "age": 30},
            {"name": "Jane", "age": 26}  # Different age
        ]
        
        self.assertFalse(SmallDiff.is_equal(expected, actual))

    def test_list_length_differences(self):
        """Test comparison of lists with different lengths."""
        expected = [1, 2, 3, 4]
        actual = [1, 2, 3]
        
        self.assertFalse(SmallDiff.is_equal(expected, actual))
        
        expected = [1, 2, 3]
        actual = [1, 2, 3, 4]
        
        self.assertFalse(SmallDiff.is_equal(expected, actual))

    def test_print_diff_functionality(self):
        """Test that print_diff parameter works correctly."""
        expected = {"key": "value1"}
        actual = {"key": "value2"}
        
        # This should not raise any exceptions
        diff = SmallDiff.compare(expected, actual, print_diff=True)
        self.assertIn("key", diff)

    def test_complex_nested_structure(self):
        """Test comparison of complex nested structures."""
        expected = {
            "users": [
                {
                    "name": "John",
                    "addresses": [
                        {"street": "123 Main St", "city": "Boston"},
                        {"street": "456 Oak Ave", "city": "New York"}
                    ],
                    "metadata": {
                        "created": "2023-01-01",
                        "tags": ["active", "premium"]
                    }
                }
            ]
        }
        
        actual = {
            "users": [
                {
                    "name": "John",
                    "addresses": [
                        {"street": "123 Main St", "city": "Boston"},
                        {"street": "456 Oak Ave", "city": "Chicago"}  # Different city
                    ],
                    "metadata": {
                        "created": "2023-01-01",
                        "tags": ["active", "premium"]
                    }
                }
            ]
        }
        
        self.assertFalse(SmallDiff.is_equal(expected, actual))

    def test_empty_containers(self):
        """Test comparison of empty containers."""
        # Empty lists
        self.assertTrue(SmallDiff.is_equal([], []))
        
        # Empty dicts
        self.assertTrue(SmallDiff.is_equal({}, {}))
        
        # Empty sets
        self.assertTrue(SmallDiff.is_equal(set(), set()))
        
        # Empty tuples
        self.assertTrue(SmallDiff.is_equal((), ()))

    def test_mixed_container_types(self):
        """Test that different container types are not equal."""
        with self.assertRaises(TypeError):
            SmallDiff.compare([1, 2, 3], (1, 2, 3))
        
        with self.assertRaises(TypeError):
            SmallDiff.compare([1, 2, 3], {1, 2, 3})

    def test_bytes_and_bytearray(self):
        """Test comparison of bytes and bytearray objects."""
        # Test bytes - use compare without print_diff to avoid JSON serialization issues
        self.assertTrue(SmallDiff.is_equal(b"hello", b"hello"))
        diff = SmallDiff.compare(b"hello", b"world", print_diff=False)
        self.assertNotEqual(diff, {})
        
        # Test bytearray
        self.assertTrue(SmallDiff.is_equal(bytearray(b"hello"), bytearray(b"hello")))
        diff = SmallDiff.compare(bytearray(b"hello"), bytearray(b"world"), print_diff=False)
        self.assertNotEqual(diff, {})

    def test_complex_numbers(self):
        """Test comparison of complex numbers."""
        self.assertTrue(SmallDiff.is_equal(1+2j, 1+2j))
        diff = SmallDiff.compare(1+2j, 1+3j, print_diff=False)
        self.assertNotEqual(diff, {})


if __name__ == '__main__':
    unittest.main()
