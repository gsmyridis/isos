from isos import Some, Null, Option, Result, Err, Ok, error


@error(message="Cannot divide by zero")
class DivisionByZero: ...


def find_user(user_id: int) -> Option[str]:
    users = {1: "Alice", 2: "Bob"}
    return Some(users[user_id]) if user_id in users else Null()


def safe_divide(a: float, b: float) -> Result[float]:
    if b == 0:
        return Err(DivisionByZero())
    return Ok(a / b)


def describe_user(user_opt: Option[str]) -> str:
    match user_opt:
        case Some(name):
            return f"User found: {name}"
        case Null():
            return "No user found"
        case _:
            raise TypeError("user_opt is not an Option")


def handle_division(result: Result[float]):
    match result:
        case Ok(value):
            return f"Success: {value}"
        case Err(error):
            return f"Failed: {error}"
        case _:
            raise TypeError("result is not a result")


def test_user():
    user = find_user(1)
    if user.is_some():
        print(f"Found user: {user.unwrap()}")
    else:
        print("User not found")

    name = find_user(42).unwrap_or("Guest")
    assert name == "Guest"


def test_db_pattern_matching():
    assert describe_user(Some("Alice")) == "User found: Alice"
    assert describe_user(Null()) == "No user found"


def test_safe_division():
    result = safe_divide(10, 2)
    assert result.is_ok()

    result = safe_divide(10, 0).map(lambda x: x * 2)
    assert result == Err(DivisionByZero())

    result = safe_divide(20, 2).and_then(lambda x: safe_divide(x, 2))
    assert result == Ok(5.0)


def test_safe_division_handle():
    assert handle_division(safe_divide(10, 2)) == "Success: 5.0"
    assert handle_division(safe_divide(1, 0)) == "Failed: Cannot divide by zero"
