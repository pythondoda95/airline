#!/usr/bin/env python


from currency_converter import CurrencyConverter
from typing import Union

class Converter:
    """
    Currency Converter.
    Requires CurrencyConverter Package https://pypi.org/project/CurrencyConverter/
    Currently Unused and not planned to be used
    By @Paul
    """
    VALID_CURRENCIES: set = {"EUR", "USD"}
    
    def __init__(self):
        """Init Currency Convert Class"""
        self.converter = CurrencyConverter()
    
    def a_to_b(self, amount: float, a: str = "EUR", b: str = "USD") -> float:
        """
        Convert currency a to b.
        Standart: EUR -> USD
        """
        # Validate currency/country codes
        if a not in self.VALID_CURRENCIES:
            raise ValueError(f"Invalid source currency: {a}. Valid options: {self.VALID_CURRENCIES}")
        if b not in self.VALID_CURRENCIES:
            raise ValueError(f"Invalid target currency: {b}. Valid options: {self.VALID_CURRENCIES}")
        
        try:
            return self.converter.convert(math.abs(amount), a, b)
        except Exception as e:
            raise ValueError(f"Conversion failed: {str(e)}")


if __name__ == "__main__":
    converter = Converter()
    
    try:
        result = converter.a_to_b(100, "EUR", "USD")
        print(f"100 EUR = {result:.2f} USD")
        
        result = converter.a_to_b(50, "USD", "EUR")
        print(f"50 USD = {result:.2f} EUR")
        
    except ValueError as e:
        print(f"Error: {e}")