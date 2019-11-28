from convert_codemeta import validate_codemeta, crosswalk
import pytest
import json


def test_basic_convert():
    with open("tests/package.json") as infile:
        data = json.load(infile)
        codemeta = crosswalk(data, "NodeJS")
        result = validate_codemeta(codemeta)
        assert result == True


def test_biotools_convert():
    with open("tests/integron_finder.biotools.json") as infile:
        data = json.load(infile)
        codemeta = crosswalk(data, "bio.tools")
        result = validate_codemeta(codemeta)
        assert result == True
        with open("tests/codemeta_biotools.json", "r") as compfile:
            comp = json.load(compfile)
            assert comp == codemeta
        # json.dump(codemeta,outfile)
