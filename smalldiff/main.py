import json
from typing import Any, Type

from smalldiff.encoder import ModelEncoder


class SmallDiff:

    @classmethod
    def is_equal(cls, expected: Any, actual: Any,
                 encoder: Type[ModelEncoder] = None) -> bool:
        """
        returns True if the difference is None,
        can be used for Testing object equality
        """
        return not cls.compare(expected, actual, print_diff=True, encoder=encoder)

    @classmethod
    def compare(cls, expected: Any, actual: Any,
                print_diff: bool = False,
                encoder: Type[ModelEncoder] = None) -> dict:
        """
        Takes to objects and converts into a dictionary.
        Then check the equality between dictionaries
        """
        expected_dict: dict = cls.__to_dict(expected, encoder)
        actual_dict: dict = cls.__to_dict(actual, encoder)

        if expected_dict == actual_dict:
            return {}
        else:
            diff: dict = cls.__dict_diff(expected_dict, actual_dict)
            if print_diff:
                cls.__print_diff(diff)
            return diff

    @classmethod
    def __to_dict(cls,
                  schema: Any,
                  encoder: Type[ModelEncoder] = None) -> dict:
        if encoder:
            return json.loads(json.dumps(schema, cls=encoder, indent=4))
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

            elif isinstance(val, list) and key in actual and isinstance(actual[key], list):
                list_diff = cls.__list_diff(expected=val, actual=actual[key], path=f"{path}.{key}" if path else key)
                if list_diff:
                    diff.update(list_diff)

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
    def __list_diff(cls, expected: list, actual: list, path="") -> dict:
        """
        Compares two lists and returns a dictionary of their differences.
        """
        diff = {}
        for i, (expected_val, actual_val) in enumerate(zip(expected, actual)):
            # Check if the expected value in the list is a dictionary and if it exists in the actual list
            # If both conditions are true, recursively call the dict_diff function with the nested dictionary
            # and update the diff dictionary with the returned values
            if isinstance(expected_val, dict) and isinstance(actual_val, dict):
                nested_diff = cls.__dict_diff(expected=expected_val, actual=actual_val,
                                              path=f"{path}.{i}" if path else i)
                if nested_diff:
                    diff.update(nested_diff)

            # Check if the expected value in the list does not match the actual value in the list
            elif expected_val != actual_val:
                diff[f"{path}.{i}" if path else i] = {"expected": expected_val, "actual": actual_val}

        # Check if the actual list has more elements than the expected list
        # If true, add the extra elements to the diff dictionary
        if len(actual) > len(expected):
            for j in range(len(expected), len(actual)):
                diff[f"{path}.{j}" if path else j] = {"expected": None, "actual": actual[j]}

        return diff

    @classmethod
    def __print_diff(cls, diff: dict):
        print(f"\n============================= expected vs actual ==============================")
        print(json.dumps(diff, indent=2))
