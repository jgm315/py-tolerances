class ValTol:
    def __init__(self, nominal, min_value, max_value):
        self.nominal = nominal
        self.min_value = min_value
        self.max_value = max_value

    def __repr__(self):
        # Limit values to six significant digits
        nominal_str = f"{self.nominal:.6g}"
        min_str = f"{self.min_value:.6g}"
        max_str = f"{self.max_value:.6g}"

        # Calculate margins
        margin_min = self.nominal - self.min_value
        margin_max = self.max_value - self.nominal

        # Format margin to six significant digits
        margin_min_str = f"{margin_min:.6g}"
        margin_max_str = f"{margin_max:.6g}"

        # Return formatted string with ± margins
        return f"Nominal: {nominal_str}, (-{margin_min_str} / +{margin_max_str})"

    # Addition
    def __add__(self, other):
        if isinstance(other, (int, float)):
            return utol(self.nominal + other,
                        self.min_value + other,
                        self.max_value + other)
        elif isinstance(other, utol):
            return utol(self.nominal + other.nominal,
                        self.min_value + other.min_value,
                        self.max_value + other.max_value)
        else:
            raise TypeError("Unsupported operand type(s) for +: 'utol' and other")

    # Subtraction
    def __sub__(self, other):
        if isinstance(other, (int, float)):
            return utol(self.nominal - other,
                        self.min_value - other,
                        self.max_value - other)
        elif isinstance(other, utol):
            return utol(self.nominal - other.nominal,
                        self.min_value - other.max_value,
                        self.max_value - other.min_value)
        else:
            raise TypeError("Unsupported operand type(s) for -: 'utol' and other")

    # Multiplication
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            nominal = self.nominal * other
            combinations = [self.min_value * other,
                            self.max_value * other]
            return utol(nominal, min(combinations), max(combinations))
        elif isinstance(other, utol):
            nominal = self.nominal * other.nominal
            combinations = [self.min_value * other.min_value,
                            self.min_value * other.max_value,
                            self.max_value * other.min_value,
                            self.max_value * other.max_value]
            return utol(nominal, min(combinations), max(combinations))
        else:
            print(type(other))
            raise TypeError("Unsupported operand type(s) for *: 'utol' and other")

        # Normal division (utol / something else)

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            nominal = self.nominal / other
            min_val = self.min_value / other
            max_val = self.max_value / other
            return utol(nominal, min_val, max_val)
        elif isinstance(other, utol):
            nominal = self.nominal / other.nominal
            combinations = [self.min_value / other.min_value,
                            self.min_value / other.max_value,
                            self.max_value / other.min_value,
                            self.max_value / other.max_value]
            return utol(nominal, min(combinations), max(combinations))
        else:
            raise TypeError("Unsupported operand type(s) for /: 'utol' and other")

        # Reverse division (something else / utol)

    def __rtruediv__(self, other):
        if isinstance(other, (int, float)):
            nominal = other / self.nominal
            combinations = [other / self.max_value,
                            other / self.min_value]
            return utol(nominal, min(combinations), max(combinations))
        else:
            raise TypeError("Unsupported operand type(s) for /: 'utol' and other")

    # Exponentiation
    def __pow__(self, exponent):
        if isinstance(exponent, (int, float)):
            # If the exponent is a simple number
            nominal = self.nominal ** exponent
            combinations = [self.min_value ** exponent,
                            self.max_value ** exponent]
            return utol(nominal, min(combinations), max(combinations))

        elif isinstance(exponent, utol):
            # If the exponent is another 'utol' instance, consider all combinations
            combinations = [
                self.min_value ** exponent.min_value,
                self.min_value ** exponent.max_value,
                self.max_value ** exponent.min_value,
                self.max_value ** exponent.max_value
            ]
            # Handle the nominal value separately
            nominal = self.nominal ** exponent.nominal
            return utol(nominal, min(combinations), max(combinations))
        else:
            raise TypeError("Exponent must be an integer, float, or 'utol' instance")
