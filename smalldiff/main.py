import json
from typing import Any, Type

from pydantic.main import BaseModel

from smalldiff.encoder import ModelEncoder


class SmallDiff:

    @classmethod
    def is_equal(cls, expected: Any, actual: Any) -> bool:
        """
        returns True if the difference is None
        """
        return not cls.compare(expected, actual, print_diff=True)

    @classmethod
    def compare(cls, expected: Any, actual: Any, print_diff: bool = False) -> dict:
        """
        Takes to objects and converts into a dictionary.
        Then check the equality between dictionaries
        """
        expected_dict: dict = cls.__to_dict(expected)
        actual_dict: dict = cls.__to_dict(actual)

        if expected_dict == actual_dict:
            return {}
        else:
            diff: dict = cls.__dict_diff(expected_dict, actual_dict)
            if print_diff:
                cls.__print_diff(diff)
            return diff

    @classmethod
    def __to_dict(cls, schema: Any, encoder: Type[ModelEncoder] = None) -> dict:
        if encoder:
            return json.loads(json.dumps(schema, cls=encoder, indent=4))
        if isinstance(schema, BaseModel):
            return json.loads(schema.json())
        if isinstance(schema, Exception):
            return vars(schema)
        return json.loads(json.dumps(schema, cls=ModelEncoder, indent=4))

    @classmethod
    def __dict_diff(cls, expected: dict, actual: dict, path="") -> dict:
        """
        Recursively compares two dictionaries and returns a dictionary of their differences.
        """
        diff = {}
        # First iterate the expected dictionary
        for key, val in expected.items():

            # 1. Check if the value of the key is a dictionary and if it exists in the actual dictionary
            # 2. If both conditions are true, recursively call the dict_diff function with the nested dictionary
            # 3. and update the diff dictionary with the returned values
            if isinstance(val, dict) and key in actual and isinstance(actual[key], dict):
                nested_diff = cls.__dict_diff(expected=val, actual=actual[key], path=f"{path}.{key}" if path else key)
                if nested_diff:
                    diff.update(nested_diff)

            # Check if the key is not present in the actual dictionary
            # If true, add the key and its expected value to the diff dictionary
            elif key not in actual:
                diff[f"{path}.{key}" if path else key] = {"expected": val, "actual": None}

            # Check if the expected value of the key does not match the actual value of the key
            # If true, add the key and its expected and actual values to the diff dictionary
            elif val != actual[key]:
                diff[f"{path}.{key}" if path else key] = {"expected": val, "actual": actual[key]}

        # Check for keys in the actual dictionary that are not present in the expected dictionary
        # If true, add the key and its actual value to the diff dictionary
        for key, val in actual.items():
            if key not in expected:
                diff[f"{path}.{key}" if path else key] = {"expected": None, "actual": val}

        return diff

    @classmethod
    def __print_diff(cls, diff: dict):
        print(f"\n============================= expected vs actual ==============================")
        print(json.dumps(diff, indent=2))
