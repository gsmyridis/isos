import re
import pytest
from isos import (
    Option,
    UnwrapError,
    Null,
    Some,
    UNWRAP_OPTION_MSG,
    Ok,
    Err,
    NotComparableError,
)


def test_eq():
    assert Null() == Null()
    assert Some(10) == Some(10)


def test_neq():
    assert Some(10) != Some(20)
    assert Some(10) != Null()


def test_less_than_success():
    assert Some(10).less_than(Some(20)) == Ok(True)
    assert Null[int]().less_than(Some(20)) == Ok(True)

    assert Some(20).less_than(Some(10)) == Ok(False)
    assert Some(10).less_than(Some(10)) == Ok(False)
    assert Null[int]().less_than(Null[int]()) == Ok(False)
    assert Some(20).less_than(Null[int]()) == Ok(False)


def test_less_than_fail():
    assert Some(1 + 2j).less_than(Some(3 + 6j)) == Err(NotComparableError())


def test_less_than_unsafe_success():
    assert Some(10).less_than_unsafe(Some(20))
    assert Null[int]().less_than_unsafe(Some(20))

    assert not Some(20).less_than_unsafe(Some(10))
    assert not Some(10).less_than_unsafe(Some(10))
    assert not Null[int]().less_than_unsafe(Null[int]())
    assert not Some(20).less_than_unsafe(Null[int]())


def test_less_than_unsafe_fail():
    with pytest.raises(TypeError):
        _ = Some(1 + 2j).less_than_unsafe(Some(3 + 6j))


def test_less_or_equal_success():
    assert Some(10).less_or_equal(Some(20)) == Ok(True)
    assert Some(10).less_or_equal(Some(10)) == Ok(True)
    assert Null[int]().less_or_equal(Some(20)) == Ok(True)
    assert Null[int]().less_or_equal(Null[int]()) == Ok(True)


def test_less_or_equal_fail():
    assert Some(1 + 2j).less_or_equal(Some(10)) == Err(NotComparableError())


def test_less_or_equal_unsafe_success():
    assert Some(10).less_or_equal_unsafe(Some(20))
    assert Some(10).less_or_equal_unsafe(Some(10))
    assert Null[int]().less_or_equal_unsafe(Some(20))
    assert Null[int]().less_or_equal_unsafe(Null[int]())


def test_less_or_equal_unsafe_fail():
    with pytest.raises(TypeError):
        _ = Some(1 + 2j).less_or_equal_unsafe(Some(10))


def test_greater_than_unsafe_success():
    assert Some(10).greater_than_unsafe(Some(0))
    assert Some(10).greater_than_unsafe(Null[int]())

    assert not Some(0).greater_than_unsafe(Some(10))
    assert not Some(10).greater_than_unsafe(Some(10))
    assert not Null[int]().greater_than_unsafe(Some(10))
    assert not Null[int]().greater_than_unsafe(Null[int]())


def test_greater_than_unsafe_fail():
    with pytest.raises(TypeError):
        _ = Some(1 + 2j).greater_than_unsafe(Some(0))


def test_greater_than_success():
    assert Some(10).greater_than(Some(0)) == Ok(True)
    assert Some(10).greater_than(Null[int]()) == Ok(True)

    assert Some(0).greater_than(Some(10)) == Ok(False)
    assert Some(10).greater_than(Some(10)) == Ok(False)
    assert Null[int]().greater_than(Some(10)) == Ok(False)
    assert Null[int]().greater_than(Null[int]()) == Ok(False)


def test_greater_than_fail():
    assert Some(10).greater_than(Some(1 + 2j)) == Err(NotComparableError())


def test_greater_or_equal_unsafe_success():
    assert Some(10).greater_or_equal_unsafe(Some(0))
    assert Some(10).greater_or_equal_unsafe(Null[int]())
    assert Some(10).greater_or_equal_unsafe(Some(10))
    assert Null[int]().greater_or_equal_unsafe(Null[int]())

    assert not Some(0).greater_or_equal_unsafe(Some(10))
    assert not Null[int]().greater_or_equal_unsafe(Some(10))


def test_greater_or_equal_unsafe_fail():
    with pytest.raises(TypeError):
        _ = Some(1 + 2j).greater_or_equal_unsafe(Some(0))


def test_greater_or_equal_success():
    assert Some(10).greater_or_equal(Some(0)) == Ok(True)
    assert Some(10).greater_or_equal(Null[int]()) == Ok(True)
    assert Some(10).greater_or_equal(Some(10)) == Ok(True)
    assert Null[int]().greater_or_equal(Null[int]()) == Ok(True)

    assert Some(0).greater_or_equal(Some(10)) == Ok(False)
    assert Null[int]().greater_or_equal(Some(10)) == Ok(False)


def test_greater_or_equal_fail():
    assert Some(1 + 2j).greater_or_equal(Some(0)) == Err(NotComparableError())


def test_option_is_none():
    assert Null().is_none()
    assert not Some(10).is_none()


def test_option_is_some():
    assert not Null().is_some()
    assert Some(10).is_some()


def test_is_some_and():
    assert Some(10).is_some_and(lambda x: x > 5)

    assert not Some(10).is_some_and(lambda x: x > 20)
    assert not Null[int]().is_some_and(lambda x: x > -1)


def test_is_none_or():
    assert Null[int]().is_none_or(lambda x: x > -1)
    assert Some(10).is_none_or(lambda x: x > 5)

    assert not Some(10).is_none_or(lambda x: x > 20)


def test_expect_unwrap():
    expect_msg = "Guaranteed to be some value."
    assert Some(10).expect(expect_msg) == 10
    assert Some(10).unwrap() == 10

    with pytest.raises(UnwrapError, match=expect_msg):
        _ = Null[int]().expect(expect_msg)
    with pytest.raises(UnwrapError, match=re.escape(UNWRAP_OPTION_MSG)):
        _ = Null[int]().unwrap()


def test_unwrap_or():
    assert Some(10).unwrap_or(20) == 10
    assert Null[int]().unwrap_or(20) == 20


def test_unwrap_or_else():
    def func() -> int:
        return 100**2 - 9000

    assert Some(10).unwrap_or_else(func) == 10
    assert Null().unwrap_or_else(func) == 1000


def test_map():
    def get_len(s: str) -> int:
        return len(s)

    assert Some("abc").map(get_len).unwrap() == 3
    assert Null[str]().map(get_len).is_none()


def test_map_or():
    def get_len(s: str) -> int:
        return len(s)

    assert Some("abc").map_or(0, get_len) == 3
    assert Null[str]().map_or(0, get_len) == 0


def test_map_or_else():
    def handle_some(x: float) -> str:
        return "Passed" if x >= 5 else "Failed"

    def handle_none() -> str:
        return "Failed"

    assert Some(4.9).map_or_else(handle_none, handle_some) == "Failed"


def test_and():
    assert Some(10).and_option(Some(20)).unwrap() == 20
    assert Null[int]().and_option(Some(20)).is_none()
    assert Some(10).and_option(Null()).is_none()


def test_and_then():
    def grade(x: float) -> Option[str]:
        return Some("Passed") if x > 5 else Some("Failed")

    assert Null[float]().and_then(grade).is_none()
    assert Some(4.9).and_then(grade).unwrap() == "Failed"
    assert Some(10).and_then(grade).unwrap() == "Passed"


def test_filter():
    def over_5(x: float) -> bool:
        return x > 5

    assert Null[float]().filter(over_5).is_none()
    assert Some(4.6).filter(over_5).is_none()
    assert Some(10).filter(over_5).unwrap() == 10


def test_or():
    assert Some(10).or_option(Some(20)).unwrap() == 10
    assert Some(10).or_option(Null()).unwrap() == 10

    assert Null[int]().or_option(Some(20)).unwrap() == 20
    assert Null[int]().or_option(Null()).is_none()


def test_or_else():
    def default() -> Option[int]:
        return Some(20)

    assert Some(10).or_else(default).unwrap() == 10
    assert Null[int]().or_else(default).unwrap() == 20


def test_xor():
    assert Some(10).xor(Some(20)).is_none()
    assert Null[int]().xor(Null()).is_none()

    assert Some(10).xor(Null()).unwrap() == 10
    assert Null[int]().xor(Some(20)).unwrap() == 20


def test_zip():
    assert Some(10).zip(Some("Passed")).unwrap() == (10, "Passed")
    assert Some(10).zip(Null[str]()).is_none()
    assert Null[int]().zip(Some("Failed")).is_none()


def test_pattern_matching():
    match Some([10, 11, 12]):
        case Some([val, *rest]):
            assert val == 10
            assert rest == [11, 12]
        case Some(val):
            assert False  # Should not reach this
