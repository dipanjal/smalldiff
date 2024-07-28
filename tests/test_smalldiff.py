import unittest
from typing import List

from schema import LocationModel, Gender
from smalldiff import SmallDiff
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


if __name__ == '__main__':
    unittest.main()
