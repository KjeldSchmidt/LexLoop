from lexloop.auth.memorable_ids import generate_password, generate_username


def test_username_is_three_hyphenated_words() -> None:
    username = generate_username()
    parts = username.split("-")
    assert len(parts) == 3
    assert all(part.isalpha() and part.islower() for part in parts)
    assert len(set(parts)) == 3


def test_password_is_four_spaced_words() -> None:
    password = generate_password()
    parts = password.split(" ")
    assert len(parts) == 4
    assert all(part.isalpha() and part.islower() for part in parts)
    assert "-" not in password


def test_username_and_password_shapes_differ() -> None:
    username = generate_username()
    password = generate_password()
    assert "-" in username
    assert " " not in username
    assert " " in password
    assert "-" not in password
