import unittest

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
            )
        )
        person2 = PersonModel(
            name="John Doe",
            age=27,
            address=AddressModel(
                street="123 Main St.",
                dist="Magura",
                zip=7600
            )
        )
        assert not SmallDiff.is_equal(person1, person2)
        # self.assertEqual(person1, person2)


if __name__ == '__main__':
    unittest.main()
