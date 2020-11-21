from convert_codemeta import convert


def test_deep_get():
    data = {"data": {"files": [1, 2, 3]}}
    assert convert.deep_get(data, "data.files.0") == 1
    assert convert.deep_get(data, "data.files.1") == 2
    assert convert.deep_get(data, "data.files") == [1, 2, 3]
    assert convert.deep_get(data, "data") == {"files": [1, 2, 3]}


def test_deep_put():
    data = {}
    assert convert.deep_put(data, "data.files.fun", 0) == {
        "data": {"files": {"fun": 0}}
    }
    data = {}
    assert convert.deep_put(data, "data.files", 0) == {"data": {"files": 0}}
    assert convert.deep_put(data, "data.fun", 1) == {"data": [{"files": 0}, {"fun": 1}]}


test_deep_get()
test_deep_put()
