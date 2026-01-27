# pyGr utilities

A collection of Python utilities for handling Greek-specific data formats, including date/time conversions, number formatting, text normalization, and validators.

## Installation

### As a Git Submodule

From your project root run:

```bash
git submodule add https://github.com/tedlaz/pygr.git
```

In order to sync it with GitHub run:

```bash
git submodule update --remote --recursive
```

## Modules

### `utils.texts`

Functions for Greek text normalization and comparison.

- **`grup(text: str) -> str`**
  Returns uppercase text with Greek diacritical marks removed for normalized comparison.
  Example: `grup("Καλημέρα")` → `"ΚΑΛΗΜΕΡΑ"`

- **`is_text_same(text1: str, text2: str) -> bool`**
  Case-insensitive comparison of two strings, handling special Greek characters.
  Example: `is_text_same("Καλημέρα", "καλημερα")` → `True`

### `utils.datetimes`

Functions for date/time conversions and calculations.

- **`iso2gr(iso_date_str: str) -> str`**
  Convert ISO 8601 date (YYYY-MM-DD) to Greek format (DD/MM/YYYY).
  Example: `iso2gr("2024-06-15")` → `"15/06/2024"`

- **`gr2iso(gr_date: str) -> str`**
  Convert Greek date format (DD/MM/YYYY) to ISO 8601 (YYYY-MM-DD).
  Example: `gr2iso("15/06/2024")` → `"2024-06-15"`

- **`date2gr(date_obj: datetime.date) -> str`**
  Convert a date object to Greek date string (DD/MM/YYYY).

- **`gr2date(gr_date: str) -> datetime.date`**
  Convert Greek date string (DD/MM/YYYY) to a date object.

- **`iso2yearmonth(isodate: str) -> str`**
  Extract year-month from ISO date.
  Example: `iso2yearmonth("2024-06-15")` → `"2024-06"`

- **`is_greek_date(grdate: str) -> bool`**
  Check if string matches Greek date format (DD/MM/YYYY).

- **`delta_hours(date_from: datetime, date_to: datetime) -> float`**
  Calculate absolute hours between two datetime objects.

- **`round_half(hours: float) -> float`**
  Round hours to nearest half hour.
  Example: `round_half(2.3)` → `2.5`

- **`month_monday2friday_days(year: int, month: int) -> int`**
  Calculate number of weekdays (Monday-Friday) in a given month.

- **`month_specific_days(year: int, month: int, weekdays: set[int]) -> int`**
  Count specific weekdays in a month (0=Monday, 6=Sunday).

- **`month_specific_days_gr(year: int, month: int, wdays: str) -> int`**
  Count specific weekdays using Greek day names.
  Examples:
  - `"ΔΕΥΤΕΡΑ-ΠΑΡΑΣΚΕΥΗ"` (Monday to Friday)
  - `"ΔΕΥΤΕΡΑ,ΤΕΤΑΡΤΗ,ΠΑΡΑΣΚΕΥΗ"` (Monday, Wednesday, Friday)
  - `"ΠΑΡΑΣΚΕΥΗ"` (Friday only)

### `utils.numbers`

Functions for Greek number format conversions.

- **`gr2float(gr_number_str: str) -> float`**
  Convert Greek-formatted number (1.234.567,89) to float.
  Example: `gr2float("1.234,56")` → `1234.56`

- **`float2gr(number: float, decimals=2) -> str`**
  Convert float to Greek-formatted string (1.234.567,89).
  Example: `float2gr(1234.56)` → `"1.234,56"`

- **`float2gr_empty_zero(number: float, decimals=2) -> str`**
  Same as float2gr but returns empty string for zero values.

### `utils.validators`

Validators for Greek identification numbers.

- **`is_valid_afm(afm: str) -> bool`**
  Algorithmic validation of Greek VAT number (AFM - 9 digits).
  Example: `is_valid_afm("012312312")` → `True`

- **`is_valid_amka(amka: str) -> bool`**
  Algorithmic validation of Greek Social Security Number (AMKA - 11 digits).
  Example: `is_valid_amka("13080002382")` → `True`

## Usage Examples

```python
from utils.texts import grup, is_text_same
from utils.datetimes import iso2gr, gr2iso
from utils.numbers import gr2float, float2gr
from utils.validators import is_valid_afm, is_valid_amka

# Text normalization
normalized = grup("Καλημέρα")  # "ΚΑΛΗΜΕΡΑ"
are_same = is_text_same("Άνθρωπος", "ανθρωπος")  # True

# Date conversions
greek_date = iso2gr("2024-06-15")  # "15/06/2024"
iso_date = gr2iso("15/06/2024")  # "2024-06-15"

# Number formatting
price = gr2float("1.234,56")  # 1234.56
formatted = float2gr(1234.56)  # "1.234,56"

# Validators
valid_vat = is_valid_afm("012312312")  # True
valid_ssn = is_valid_amka("13080002382")  # True
```

## Testing

Run tests with pytest:

```bash
uv run pytest -v
```

## License

MIT
