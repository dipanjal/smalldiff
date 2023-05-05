# SmallDiff

SmallDiff is a Python library inspired by **_assertJ_** that provides a simple way to identify differences between two Python objects. It is designed to be easy to use and highly flexible, allowing you to compare objects of any type, including dictionaries, lists, and custom classes. SmallDiff uses a recursive algorithm to compare the values of the objects and return a map of the differences. With SmallDiff, you can quickly identify the changes between two objects and take appropriate action. Whether you're working on a small script or a large project, SmallDiff can help you write more robust and reliable code.

## Installation

First, ensure that you have Python 3.x installed on your system. You can check your version of Python by running:

```
python --version
```

If you have multiple versions of Python installed, you can use `pyenv` to manage your versions. To install `pyenv`, follow the instructions in the [official documentation](https://github.com/pyenv/pyenv#installation).

Next, you'll need to install `pipenv` for virtual environment and dependency management. To install `pipenv`, run:

```
pip install pipenv
```

Once you have `pipenv` installed, you can use a `make` command to create a new virtual environment for this project and install the dependencies. But make sure you have `make` installed in your system


### Mac/Linux

On Mac/Linux, you can install the project and its dependencies by running:
```
make install
```


### Windows

On Windows, you'll need to install GNU Make and run it from the command prompt. You can download GNU Make from the [official website](http://gnuwin32.sourceforge.net/packages/make.htm). Once you have GNU Make installed, you can navigate to the project directory and run:

```
make install
```


This will create a new virtual environment and install the dependencies listed in the `Pipfile.lock` file.

## Usage

To use this library, you can import the `compare` function from the `smalldiff.SmallDiff` module:

Example 1: Comparing two dictionaries with nested items
```python
from smalldiff import SmallDiff

# the data we expect
expected = {
    "name": "John Doe",
    "age": 28,
    "address": {
        "street": "123 Main St.",
        "dist": "Dhaka",
        "zip": 1227
    }
}

# the actual data we get maybe after an API call
actual = {
    "name": "John Doe",
    "age": 28,
    "address": {
        "street": "123 Main St.",
        "dist": "Magura",
        "zip": 7600
    }
}
diff = SmallDiff.compare(expected, actual)
print(diff)
```

`output`
```json
{
    "address.dist": {
        "expected": "Dhaka",
        "actual": "Magura",
    },
    "address.zip": {
        "expected": 1227,
        "actual": 7600,
    }
}
```
We can also use it to assert test cases. See an example bellow
https://github.com/dipanjal/smalldiff/blob/b9fff41b95d102fb610a2b732287220dac83fd37/tests/test_smalldiff.py#L13-L33
