def gr2float(gr_number_str: str) -> float:
    """Convert a Greek-formatted number string (1.234.567,89) to a float representation."""
    no_thousands = gr_number_str.replace(".", "")
    standard_format = no_thousands.replace(",", ".")
    return float(standard_format)


def float2gr(number: float, decimals=2) -> str:
    """Convert a float number to a Greek-formatted number string (1.234.567,89)."""
    standard_format = f"{number:,.{decimals}f}"
    gr_format = standard_format.replace(",", "X").replace(".", ",").replace("X", ".")
    return gr_format


def float2gr_empty_zero(number: float, decimals=2) -> str:
    """Convert a float number to a Greek-formatted number string (1.234.567,89)."""
    if number == 0:
        return ""
    return float2gr(number, decimals)
