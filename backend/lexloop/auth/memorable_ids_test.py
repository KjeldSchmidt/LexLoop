from lexloop.auth.memorable_ids import generate_password, generate_username


def test_username_is_pascal_case_adjective_noun() -> None:
    username = generate_username()
    assert "-" not in username
    assert " " not in username
    assert username[0].isupper()
    assert any(ch.islower() for ch in username)
    assert username.isalnum()


def test_username_numeric_suffix() -> None:
    username = generate_username(with_numeric_suffix=True)
    assert username[-2:].isdigit()
    assert 10 <= int(username[-2:]) <= 99


def test_password_is_spaced_passphrase() -> None:
    password = generate_password()
    parts = password.split(" ")
    assert len(parts) == 4
    assert all(len(part) > 0 for part in parts)
    assert "-" not in password
    assert len(password) >= 8


def test_username_and_password_shapes_differ() -> None:
    username = generate_username()
    password = generate_password()
    assert username[:1].isupper()
    assert " " not in username
    assert " " in password
