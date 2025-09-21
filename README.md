# isos

`isos` is a lightweight Python library that brings the Result Pattern to your code.
It introduces two core types — Option and Result — which behave as sum types (also known as tagged unions or discriminated unions) that make handling missing values and errors explicit, safe, and expressive.

Sum types allow you to represent values that can be one of several variants, where each variant can hold different types of data. This is particularly useful for modeling scenarios where a value can be in different states, like presence/absence (Option) or success/failure (Result).

## Why use the Result pattern?

In Python, a function can return `Optional[T]` — either a value of type `T` or `None`.
But unless you enforce strict type checking, there’s no clear indication that the value may be absent.
This often leads to `AttributeError` or `TypeError` when `None` sneaks through.

Similarly, Python uses exceptions to signal errors, but you don’t always know when a function might raise one.
You either have to read the source or wrap everything in a `try/except`.

By returning a `Result` or `Option` instead, you:

- Make absence and errors visible in the type system.
- Force explicit handling of failure cases.
- Pass, transform, and compose results safely.
- Write code that is more predictable, robust, and self-documenting.

## Examples

### Option

```Python
from isos import Some, Null, Option

def find_user(user_id: int) -> Option[str]:
    users = {1: "Alice", 2: "Bob"}
    return Some(users[user_id]) if user_id in users else Null()

# Handling the result:
user = find_user(1)
if user.is_some():
    print(f"Found user: {user.unwrap()}")
else:
    print("User not found")

# You can also provide a default:
name = find_user(42).unwrap_or("Guest")
print(name)  # -> "Guest"
```

### Result

```Python
from isos import Ok, Err, Error, Result
from typing import final

# Define a custom error
@final
class DivisionByZero(Error):
    MESSAGE = "Cannot divide by zero"

def safe_divide(a: float, b: float) -> Result[float]:
def safe_divide(a: float, b: float) -> Result[float]:
    if b == 0:
        return Err(DivisionByZero())
    return Ok(a / b)

result = safe_divide(10, 2)

if result.is_ok():
    print(f"Result is {result.unwrap()}")
else:
    print(f"Error: {result.unwrap_error()}")

# Transforming results
result = safe_divide(10, 0).map(lambda x: x * 2)
# Still Err(DivisionByZero)

# Chaining
result = safe_divide(20, 2).and_then(lambda x: safe_divide(x, 2))
print(result)  # -> Ok(5.0)
```

### Pattern Matching

Python 3.10 introduced pattern matching, which works great with Option and Result:

```Python
from isos import Some, Null, Ok, Err

# Pattern matching with Option
def describe_user(user_opt: Option[str]) -> str:
    match user_opt:
        case Some(name):
            return f"User found: {name}"
        case Null():
            return "No user found"
        case _:
            raise TypeError("user_opt is not an Option")

print(describe_user(Some("Alice")))  # -> "User found: Alice"
print(describe_user(Null()))         # -> "No user found"

# Pattern matching with Result
def handle_division(result: Result[float]) -> str:
    match result:
        case Ok(value):
            return f"Success: {value}"
        case Err(error):
            return f"Failed: {error.MESSAGE}"
        case _:
            raise TypeError("result is not a Result")

print(handle_division(safe_divide(10, 2)))  # -> "Success: 5.0"
print(handle_division(safe_divide(1, 0)))   # -> "Failed: Cannot divide by zero"
```
