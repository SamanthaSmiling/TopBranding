"""
Test goes here
"""
import pytest
from brand_glimpse import read_file, glimpse





def test_func():
    assert read_file("data/transaction_data.csv") == True
    print("You are Reading correctly")

