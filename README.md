# isos

`isos` is a lightweight Python library that brings the Result Pattern to your code.
It introduces two core types — Option and Result — to make handling missing values and errors explicit, safe, and expressive.

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
from isos import Some, Null

def find_user(user_id: int):
    users = {1: "Alice", 2: "Bob"}
    return Some(users[user_id]) if user_id in users else Null

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
from isos import Ok, Err, Error

# Define a custom error
class DivisionByZero(Error):
    MESSAGE = "Cannot divide by zero"

def safe_divide(a: float, b: float):
    if b == 0:
        return Err(DivisionByZero())
    return Ok(a / b)

result = safe_divide(10, 2)

if result.is_ok():
    print(f"Result is {result.unwrap()}")
else:
    print(f"Error: {result.unwrap_err()}")

# Transforming results
result = safe_divide(10, 0).map(lambda x: x * 2)
# Still Err(DivisionByZero)

# Chaining
result = safe_divide(20, 2).and_then(lambda x: safe_divide(x, 2))
print(result)  # -> Ok(5.0)
```
