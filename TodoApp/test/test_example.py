import pytest

def test_equal_or_not_equal():
    assert 3 == 3
    assert 3 != 1

    assert isinstance('this is string', str)
    assert not isinstance('10', int)


def test_boolean():
    validated = True
    assert validated is True
    assert ('hello' == 'world') is False


def test_type():
    assert type('hello') is str
    assert type('world') is not int



def test_greater_than_or_equal_to():
    assert 3 > 2
    assert 3 < 5


def test_list():
    num_list = [1, 2, 3, 4, 5]
    any_list = [True, False]
    assert 1 in num_list
    assert 6 not in num_list
    assert all(num_list)
    assert not all(any_list)


class Student:
    def __init__(self, first_name: str, last_name: str, major: str, years: int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years


@pytest.fixture
def default_employee():
    return Student('John', 'Doe', 'Computer Science', 19)


def test_person_initialization(default_employee):
    assert default_employee.first_name == 'John', 'First name should be John'
    assert default_employee.last_name == 'Doe', 'Last name should be Doe'
    assert default_employee.major == 'Computer Science'
    assert default_employee.years == 19
