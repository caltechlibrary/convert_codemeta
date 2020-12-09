import copy
from pyld import jsonld


def validate_codemeta(json):
    """Check whether a codemeta json object is valid"""
    try:
        context = json["@context"]
    except:
        raise ValueError
    if context == "https://doi.org/10.5063/schema/codemeta-2.0":
        # Temp replacement for https resolution issues for schema.org
        context = "https://raw.githubusercontent.com/caltechlibrary/convert_codemeta/main/codemeta.jsonld"
        json["@context"] = context
    cp = copy.deepcopy(json)
    # Expand and contract to check mapping
    cp = jsonld.expand(cp)
    cp = jsonld.compact(cp, context)
    keys = cp.keys()
    # Using len because @type elements get returned as type
    same = len(set(keys)) == len(set(json.keys()))
    if not same:
        print("Unsupported terms in codemeta file")
        diff = set(json.keys() - set(keys))
        if "@type" in diff:
            diff.remove("@type")
        print(sorted(diff))
    fail = ":" in keys
    if fail:
        print("Not in schema")
        for k in keys:
            if ":" in k:
                print(k)
    return same and not fail
