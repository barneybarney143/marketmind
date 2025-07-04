from my_package import say_hello


def test_say_hello_default() -> None:
    assert say_hello() == "Hello, World!"


def test_say_hello_name() -> None:
    assert say_hello("Alice") == "Hello, Alice!"
