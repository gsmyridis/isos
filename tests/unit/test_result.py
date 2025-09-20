import re
import pytest
from isos import (
    Some,
    Null,
    Error,
    Ok,
    Err,
    UnwrapError,
    UNWRAP_RESULT_MSG,
    UNWRAP_ERR_RESULT_MSG,
)


class SomeError(Error):
    pass


class OtherError(Error):
    pass


def test_eq():
    assert Ok(10) == Ok(5 + 5)
    assert Err(SomeError()) == Err(SomeError())

    assert Ok(10) == Ok(10)
    assert Err(SomeError()) == Err(SomeError())


def test_neq():
    assert Ok(10) != Ok(20)
    assert Ok(10) != Err(SomeError())
    assert Err(SomeError()) != Err(OtherError())


def test_less_than():
    assert Ok(10).less_than_unsafe(Ok(20))
    assert Err(SomeError()).less_than_unsafe(Ok(20))

    assert not Ok(20).less_than_unsafe(Ok(10))
    assert not Ok(10).less_than_unsafe(Ok(10))
    assert not Err(SomeError()).less_than_unsafe(Err[int](SomeError()))
    assert not Err(SomeError()).less_than_unsafe(Err[int](OtherError()))
    assert not Ok(20).less_than_unsafe(Err(SomeError()))


def test_less_or_equal():
    assert Ok(10).less_or_equal_unsafe(Ok(20))
    assert Ok(10).less_or_equal_unsafe(Ok(10))
    assert Err[int](SomeError()).less_or_equal_unsafe(Ok(20))
    assert Err[int](SomeError()).less_or_equal_unsafe(Err(SomeError()))
    assert not Err[str](SomeError()).less_or_equal_unsafe(Err(OtherError()))


def test_greater_than():
    assert Ok(10).greater_than_unsafe(Ok(0))
    assert Ok(10).greater_than_unsafe(Err(SomeError()))


def test_greater_or_equal():
    assert Ok(10).greater_or_equal_unsafe(Ok(0))
    assert Ok(10).greater_or_equal_unsafe(Err(SomeError()))
    assert Ok(10).greater_or_equal_unsafe(Ok(10))
    assert Err[str](SomeError()).greater_or_equal_unsafe(Err(SomeError()))


def test_is_ok():
    assert Ok(1).is_ok()
    assert not Err(SomeError()).is_ok()


def test_is_ok_and():
    assert Ok(10).is_ok_and(lambda x: x > 5)
    assert not Ok(10).is_ok_and(lambda x: x > 10)
    assert not Err[int](Error()).is_ok_and(lambda x: x > 5)


def test_is_err():
    assert not Ok(1).is_error()
    assert Err(Error()).is_error()


def test_is_err_and():
    assert Err(SomeError()).is_error_and(lambda x: isinstance(x, SomeError))
    assert not Err(SomeError()).is_error_and(
        lambda x: isinstance(x, OtherError)
    )
    assert not Ok[int](10).is_error_and(lambda x: True)


def test_ok():
    assert Err(SomeError()).ok().is_none()
    assert Ok(10).ok() == Some(10)


def test_error():
    assert Err(SomeError()).error() == Some(SomeError())
    assert Ok(10).error() == Null()


def test_map():
    assert Ok("three").map(lambda s: len(s)).unwrap() == 5
    assert (
        Err[str](SomeError()).map(lambda s: len(s)).unwrap_error()
        == SomeError()
    )


def test_map_or():
    assert Ok("three").map_or(0, lambda s: len(s)) == 5
    assert Err[str](OtherError()).map_or(0, lambda s: len(s)) == 0


def test_map_or_else():
    assert Ok[str]("three").map_or_else(lambda e: 0, lambda s: len(s)) == 5
    assert (
        Err[str](OtherError()).map_or_else(lambda e: 0, lambda s: len(s)) == 0
    )


def test_map_err():
    def map_some_error(_err_1: Error) -> Error:
        return SomeError()

    assert Ok(1).map_error(map_some_error).unwrap() == 1
    assert (
        Err(SomeError()).map_error(lambda e: OtherError()).unwrap_error()
        == OtherError()
    )


def test_expect():
    msg = "Guaranteed to succeed."
    with pytest.raises(UnwrapError, match=re.escape(msg)):
        Err(SomeError()).expect(msg)


def test_unwrap():
    with pytest.raises(UnwrapError, match=re.escape(UNWRAP_RESULT_MSG)):
        Err(SomeError()).unwrap()


def test_expect_err():
    msg = "Guaranteed to fail."
    with pytest.raises(UnwrapError, match=re.escape(msg)):
        _ = Ok(1).expect_error(msg)


def test_unwrap_err():
    with pytest.raises(UnwrapError, match=re.escape(UNWRAP_ERR_RESULT_MSG)):
        _ = Ok(1).unwrap_error()


def test_unwrap_or():
    assert Ok(10).unwrap_or(0) == 10
    assert Err[int](SomeError()).unwrap_or(0) == 0


def test_unwrap_or_else():
    assert Ok(10).unwrap_or_else(lambda e: 20) == 10
    assert Err[int](SomeError()).unwrap_or_else(lambda e: 20) == 20


def test_and():
    assert Ok(10).and_result(Ok("Success")).unwrap() == "Success"
    assert Ok(10).and_result(Err[int](Error())).unwrap_error() == Error()
    assert (
        Err(SomeError()).and_result(Ok("Success")).unwrap_error() == SomeError()
    )
    assert (
        Err[str](SomeError()).and_result(Err[str](OtherError())).unwrap_error()
        == SomeError()
    )


def test_and_then():
    assert Ok(10).and_then(lambda x: Ok(x + 10)).unwrap() == 20
    assert (
        Ok(10).and_then(lambda x: Err[int](Error())).unwrap_error() == Error()
    )
    assert (
        Err[int](SomeError()).and_then(lambda x: Ok(x + 10)).unwrap_error()
        == SomeError()
    )
    assert (
        Err[int](SomeError())
        .and_then(lambda x: Err[int](OtherError()))
        .unwrap_error()
        == SomeError()
    )


def test_or():
    assert Ok(10).or_result(Ok(20)).unwrap() == 10
    assert Err[int](SomeError()).or_result(Ok(20)).unwrap() == 20
    assert (
        Err[int](SomeError()).or_result(Err[int](OtherError())).unwrap_error()
        == OtherError()
    )


def test_or_else():
    assert Ok(10).or_else(lambda e: Ok(20)).unwrap() == 10
    assert Err[int](SomeError()).or_else(lambda e: Ok(20)).unwrap() == 20
    assert (
        Err[int](SomeError())
        .or_else(lambda e: Err[int](OtherError()))
        .unwrap_error()
        == OtherError()
    )
