import unittest
from typing import List

from schema import LocationModel
from smalldiff import SmallDiff
from tests.schema import PersonModel, AddressModel


class TestSmallDiff(unittest.TestCase):

    def test_equal(self):
        # the data we expect
        person1 = PersonModel(
            name="John Doe",
            age=28,
            address=AddressModel(
                street="123 Main St.",
                dist="Dhaka",
                zip=1227
            )
        )
        person2 = PersonModel(
            name="John Doe",
            age=28,
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
        # self.assertEqual(person1, person2)


if __name__ == '__main__':
    unittest.main()
