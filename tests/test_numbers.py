import pytest

from utils.numbers import float2gr, gr2float


@pytest.mark.parametrize(
    "gr_number_str,expected_float",
    [
        ("1.234,56", 1234.56),
        ("-1.234,56", -1234.56),
        ("1.234,564", 1234.564),
        ("12.345.678,90", 12345678.90),
        ("0,99", 0.99),
    ],
)
def test_gr2float(gr_number_str, expected_float):
    assert gr2float(gr_number_str) == expected_float


@pytest.mark.parametrize(
    "number,expected_gr_str",
    [
        (1234.56, "1.234,56"),
        (-1234.56, "-1.234,56"),
        (12345678.90, "12.345.678,90"),
        (0.99, "0,99"),
        (0, "0,00"),
    ],
)
def test_float2gr(number, expected_gr_str):
    assert float2gr(number) == expected_gr_str
