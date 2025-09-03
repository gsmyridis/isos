import re
import pytest
from isos import Option, UnwrapError, Null, Some, UNWRAP_OPTION_MSG


def test_eq():
    assert Option(None) == Option(None)
    assert Option(10) == Option(10)

    assert Some(10) == Option(10)
    assert Null == Option(None)


def test_neq():
    assert Option(10) != Option(20)
    assert Option(10) != Option(None)


def test_less_than():
    assert Option(10) < Option(20)
    assert Option(None) < Option(20)

    assert not Option(20) < Option(10)
    assert not Option(10) < Option(10)
    assert not Option(None) < Option(None)
    assert not Option(20) < Option(None)


def test_less_or_equal():
    assert Option(10) <= Option(20)
    assert Option(10) <= Option(10)
    assert Option(None) <= Option(20)
    assert Option(None) <= Option(None)


def test_greater_than():
    assert Option(10) > Option(0)
    assert Option(10) > Option(None)

    assert not Option(10) < Option(10)
    assert not Option(20) < Option(10)
    assert not Option(10) < Option(None)
    assert not Option(None) < Option(None)


def test_greater_or_equal():
    assert Option(10) >= Option(0)
    assert Option(10) >= Option(None)
    assert Option(10) >= Option(10)
    assert Option(None) >= Option(None)


def test_option_is_none():
    assert Option.none().is_none()
    assert Option(None).is_none()

    assert Option.some(10).is_some()
    assert Option(10).is_some()


def test_is_some_and():
    assert Option(10).is_some_and(lambda x: x > 5)

    assert not Option(10).is_some_and(lambda x: x > 20)
    assert not Option[int](None).is_some_and(lambda x: x > -1)


def test_is_none_or():
    assert Option[int](None).is_none_or(lambda x: x > -1)
    assert Option(10).is_none_or(lambda x: x > 5)

    assert not Option(10).is_none_or(lambda x: x > 20)


def test_expect_unwrap():
    expect_msg = "Guaranteed to be some value."
    assert Option(10).expect(expect_msg) == 10
    assert Option(10).unwrap() == 10

    with pytest.raises(UnwrapError, match=expect_msg):
        _ = Option[int](None).expect(expect_msg)
    with pytest.raises(UnwrapError, match=re.escape(UNWRAP_OPTION_MSG)):
        _ = Option[int](None).unwrap()


def test_unwrap_or_():
    assert Option(10).unwrap_or(20) == 10
    assert Option[int](None).unwrap_or(20) == 20


def test_unwrap_or_else():
    def func() -> int:
        return 100**2 - 9000

    assert Option(10).unwrap_or_else(func) == 10
    assert Option(None).unwrap_or_else(func) == 1000


def test_map():
    def get_len(s: str) -> int:
        return len(s)

    assert Option("abc").map(get_len).unwrap() == 3
    assert Option[str](None).map(get_len).is_none()


def test_map_or():
    def get_len(s: str) -> int:
        return len(s)

    assert Option("abc").map_or(0, get_len) == 3
    assert Option[str](None).map_or(0, get_len) == 0


def test_map_or_else():
    def handle_some(x: float) -> str:
        return "Passed" if x >= 5 else "Failed"

    def handle_none() -> str:
        return "Failed"

    assert Option(4.9).map_or_else(handle_none, handle_some) == "Failed"


def test_and():
    assert Option(10).and_option(Option(20)).unwrap() == 20
    assert Option[int](None).and_option(Option(20)).is_none()
    assert Option(10).and_option(Option(None)).is_none()


def test_and_then():
    def grade(x: float) -> Option[str]:
        return Option("Passed") if x > 5 else Option("Failed")

    assert Option[float](None).and_then(grade).is_none()
    assert Option(4.9).and_then(grade).unwrap() == "Failed"
    assert Option(10).and_then(grade).unwrap() == "Passed"


def test_filter():
    def over_5(x: float) -> bool:
        return x > 5

    assert Option[float](None).filter(over_5).is_none()
    assert Option(4.6).filter(over_5).is_none()
    assert Option(10).filter(over_5).unwrap() == 10


def test_or():
    assert Option(10).or_option(Option(20)).unwrap() == 10
    assert Option(10).or_option(Option(None)).unwrap() == 10

    assert Option[int](None).or_option(Option(20)).unwrap() == 20
    assert Option[int](None).or_option(Option(None)).is_none()


def test_or_else():
    def default() -> Option[int]:
        return Option(20)

    assert Option(10).or_else(default).unwrap() == 10
    assert Option[int](None).or_else(default).unwrap() == 20


def test_xor():
    assert Option(10).xor(Option(20)).is_none()
    assert Option[int](None).xor(Option(None)).is_none()

    assert Option(10).xor(Option(None)).unwrap() == 10
    assert Option[int](None).xor(Option(20)).unwrap() == 20


def test_insert():
    opta = Option(10)
    assert opta.unwrap() == 10
    opta.insert(20)
    assert opta.unwrap() == 20

    optb = Option[int](None)
    assert optb.is_none()
    optb.insert(100)
    assert optb.unwrap() == 100


def test_take():
    opta = Option(10)
    assert opta.take().unwrap() == 10
    assert opta.is_none()

    optb = Option[int](None)
    assert optb.take().is_none()
    assert optb.is_none()


def test_take_if():
    opta = Option(10)
    assert opta.take_if(lambda x: x > 5).unwrap() == 10
    assert opta.is_none()

    optb = Option(10)
    assert optb.take_if(lambda x: x > 20).is_none()
    assert optb.unwrap() == 10

    optc = Option[int](None)
    assert optc.take_if(lambda x: x < 10).is_none()
    assert optc.is_none()


def test_replace():
    opta = Option(10)
    assert opta.replace(20).unwrap() == 10
    assert opta.unwrap() == 20

    optb = Option[int](None)
    assert optb.replace(100).is_none()
    assert optb.unwrap() == 100


def test_zip():
    assert Option(10).zip(Option("Passed")).unwrap() == (10, "Passed")
    assert Option(10).zip(Option[str](None)).is_none()
    assert Option[int](None).zip(Option("Failed")).is_none()


def test_pattern_matching():
    match Some(10):
        case Option(val):
            assert val == 10
        case _:
            assert False

    match Null:
        case Option(None):
            assert True
        case _:
            assert False

def test_get_or_insert():
    opt = Option[int](None)
    assert opt.get_or_insert(10) == 10
    assert opt.unwrap() == 10

    opt = Option(20)
    assert opt.get_or_insert(30) == 20
    assert opt.unwrap() == 20
