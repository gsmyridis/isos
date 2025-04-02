# isos

`isos` is a Python library that introduces `Option` and `Result` types to implement the "result pattern" in your code.

## Why Use This Pattern?

In traditional Python, errors are handled with exceptions. The result pattern takes a different approach by treating errors as values that can be:

- Passed between functions
- Transformed
- Chained together
- Explicitly handled at the appropriate point

This forces developers to consciously handle non-existent values and error conditions, leading to more robust and predictable code.

## Core Features

- **Option Type**: Explicitly represents the presence or absence of a value
- **Result Type**: Represents either a successful value or an error value
- **Custom Errors**: Create your own error types by subclassing the `Error` class

By making errors first-class citizens in your code, `isos` helps prevent bugs that might occur from unhandled edge cases and makes your error handling strategy more transparent and systematic.
