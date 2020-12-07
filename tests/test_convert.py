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


def test_zenodo_convert():
    with open("tests/codemeta.json") as infile:
        data = json.load(infile)
        result = validate_codemeta(data)
        assert result == True
        zenodo = crosswalk(data, "codemeta", "Zenodo")
        # This file has an incompatible license; should not be listed
        assert "license" not in zenodo
        with open("tests/zenodo.json", "r") as compfile:
            comp = json.load(compfile)
            assert comp == zenodo
        # json.dump(codemeta,outfile)
    with open("tests/codemeta_bigger.json") as infile:
        data = json.load(infile)
        result = validate_codemeta(data)
        assert result == True
        zenodo = crosswalk(data, "codemeta", "Zenodo")
        # This file has a compatible license; should be listed
        assert "license" in zenodo
        with open("tests/zenodo_bigger.json", "r") as compfile:
            comp = json.load(compfile)
            print(comp)
            print(zenodo)
            assert comp == zenodo


test_basic_convert()
test_biotools_convert()
test_zenodo_convert()
