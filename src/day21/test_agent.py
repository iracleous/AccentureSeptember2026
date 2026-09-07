"""
uv add --dev pytest

uv run pytest
"""


from day11.agent import calculate_calculator



def test_calculator_tool():
    result = calculate_calculator.invoke({"expression": "2 + 2"})
    assert result == "4"

def test_calculator_error():
    result = calculate_calculator.invoke({"expression": "1 / 0"})
    assert "Error" in result