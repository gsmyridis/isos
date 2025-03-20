# `optres`

`optres` is a library that provides types that have similary API with `Rust`'s `Option<T>` and `Result<T, E>` `enum` types.

## `Option[T]`

`Option[T]` is a type that represents an optional value.
It either contains a value of type `T` or it does not contain a value, in which case it is said to be `None`.
Technically, in the latter case the contained value of the `Option[T]` is `None`.


## `Result[T, E]`

`Result[T, E]` is a type that represents either success (`Ok`) or failure (`Err`).
