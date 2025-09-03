import re
import pytest
from isos import (
    Option,
    Result,
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
    assert Result(10) == Result(5 + 5)
    assert Result(SomeError()) == Result(SomeError())

    assert Ok(10) == Result(10)
    assert Err(SomeError()) == Result(SomeError())


def test_neq():
    assert Result(10) != Result(20)
    assert Result(10) != Result(SomeError())
    assert Err(SomeError()) != Err(OtherError())


def test_less_than():
    assert Result(10) < Result(20)
    assert Result(SomeError()) < Result(20)

    assert not Result(20) < Result(10)
    assert not Result(10) < Result(10)
    assert not Result(SomeError()) < Result(SomeError())
    assert not Result(SomeError()) < Result(OtherError())
    assert not Result(20) < Result(SomeError())


def test_less_or_equal():
    assert Result(10) <= Result(20)
    assert Result(10) <= Result(10)
    assert Result(SomeError()) <= Result(20)
    assert Result(SomeError()) <= Result(SomeError())
    assert not Result(SomeError()) <= Result(OtherError())


def test_greater_than():
    assert Result(10) > Result(0)
    assert Result(10) > Result(SomeError())

    assert not Result(10) < Result(10)
    assert not Result(20) < Result(10)
    assert not Result(10) < Result(SomeError())
    assert not Result(SomeError()) < Result(SomeError())


def test_greater_or_equal():
    assert Result(10) >= Result(0)
    assert Result(10) >= Result(SomeError())
    assert Result(10) >= Result(10)
    assert Result(SomeError()) >= Result(SomeError())


def test_is_ok():
    assert Result(1).is_ok()
    assert not Result(SomeError()).is_ok()


def test_is_ok_and():
    assert Result(10).is_ok_and(lambda x: x > 5)
    assert not Result(10).is_ok_and(lambda x: x > 10)
    assert not Result(Error()).is_ok_and(lambda x: x > 5)


def test_is_err():
    assert not Result(1).is_error()
    assert Result(Error()).is_error()


def test_is_err_and():
    assert Result(SomeError()).is_error_and(lambda x: isinstance(x, SomeError))
    assert not Result(SomeError()).is_error_and(
        lambda x: isinstance(x, OtherError)
    )
    assert not Result(10).is_error_and(lambda x: True)


def test_ok():
    assert Result(SomeError()).ok().is_none()
    assert Result(10).ok() == Option(10)


def test_error():
    assert Result(SomeError()).error() == Option.Some(SomeError())
    assert Result(10).error() == Option.none()


def test_map():
    assert Result("three").map(lambda s: len(s)).unwrap() == 5
    assert (
        Result[str](SomeError()).map(lambda s: len(s)).unwrap_error()
        == SomeError()
    )


def test_map_or():
    assert Result("three").map_or(0, lambda s: len(s)) == 5
    assert Result[str](OtherError()).map_or(0, lambda s: len(s)) == 0


def test_map_or_else():
    assert Result("three").map_or_else(lambda e: 0, lambda s: len(s)) == 5
    assert (
        Result[str](OtherError()).map_or_else(lambda e: 0, lambda s: len(s))
        == 0
    )


def test_map_err():
    assert Result(1).map_error(lambda e: SomeError()).unwrap() == 1
    assert (
        Result(SomeError()).map_error(lambda e: OtherError()).unwrap_error()
        == OtherError()
    )


def test_expect():
    msg = "Guaranteed to succeed."
    with pytest.raises(UnwrapError, match=re.escape(msg)):
        Result(SomeError()).expect(msg)


def test_unwrap():
    with pytest.raises(UnwrapError, match=re.escape(UNWRAP_RESULT_MSG)):
        Result(SomeError()).unwrap()


def test_expect_err():
    msg = "Guaranteed to fail."
    with pytest.raises(UnwrapError, match=re.escape(msg)):
        Result(1).expect_error(msg)


def test_unwrap_err():
    with pytest.raises(UnwrapError, match=re.escape(UNWRAP_ERR_RESULT_MSG)):
        Result(1).unwrap_error()


def test_unwrap_or():
    assert Result(10).unwrap_or(0) == 10
    assert Result[int](SomeError()).unwrap_or(0) == 0


def test_unwrap_or_else():
    assert Result(10).unwrap_or_else(lambda e: 20) == 10
    assert Result[int](SomeError()).unwrap_or_else(lambda e: 20) == 20


def test_and():
    assert Result(10).and_result(Result("Success")).unwrap() == "Success"
    assert Result(10).and_result(Result(Error())).unwrap_error() == Error()
    assert (
        Result(SomeError()).and_result(Result("Success")).unwrap_error()
        == SomeError()
    )
    assert (
        Result(SomeError()).and_result(Result(OtherError())).unwrap_error()
        == SomeError()
    )


def test_and_then():
    assert Result(10).and_then(lambda x: Result(x + 10)).unwrap() == 20
    assert (
        Result(10).and_then(lambda x: Result(Error())).unwrap_error() == Error()
    )
    assert (
        Result[int](SomeError())
        .and_then(lambda x: Result(x + 10))
        .unwrap_error()
        == SomeError()
    )
    assert (
        Result[int](SomeError())
        .and_then(lambda x: Result(OtherError()))
        .unwrap_error()
        == SomeError()
    )


def test_or():
    assert Result(10).or_result(Result(20)).unwrap() == 10
    assert Result[int](SomeError()).or_result(Result(20)).unwrap() == 20
    assert (
        Result(SomeError()).or_result(Result(OtherError())).unwrap_error()
        == OtherError()
    )


def test_or_else():
    assert Result(10).or_else(lambda e: Result(20)).unwrap() == 10
    assert Result[int](SomeError()).or_else(lambda e: Result(20)).unwrap() == 20
    assert (
        Result(SomeError())
        .or_else(lambda e: Result(OtherError()))
        .unwrap_error()
        == OtherError()
    )
