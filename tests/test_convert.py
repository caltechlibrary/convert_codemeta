from convert_codemeta import validate_codemeta, crosswalk
import pytest
import json


def test_basic_convert():
    with open('tests/package.json') as infile:
        data = json.load(infile)
        codemeta = crosswalk(data,"NodeJS")
        result = validate_codemeta(codemeta)
        assert result == True

