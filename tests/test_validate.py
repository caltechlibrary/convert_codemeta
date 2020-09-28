from convert_codemeta import validate_codemeta
import pytest
import json


def test_valid():
    with open("tests/codemeta.json") as infile:
        data = json.load(infile)
        result = validate_codemeta(data)
        assert result == True


def test_junk(capsys):
    with open("tests/junk_codemeta.json") as infile:
        data = json.load(infile)
        result = validate_codemeta(data)
        assert result == False
        captured = capsys.readouterr()
        print(captured.out)
        assert (
            captured.out
            == "Unsupported terms in \
codemeta file\n['codeRepo', 'descr', 'issueTrack', 'na']\n"
        )
