"""
uv add --dev pytest
uv run pytest
"""


from day21.agent import calculate_calculator



def test_calculator_tool():
    result = calculate_calculator.invoke({"expression": "2 + 2"})
    assert result == "4"

def test_calculator_error():
    result = calculate_calculator.invoke({"expression": "1 / 0"})
    assert "Error" in result

def test_calculator_error22():
    result = calculate_calculator.invoke({"expression": "1 / 0"})
    assert "Error" in result    

 #comment   git 