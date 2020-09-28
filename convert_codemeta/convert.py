from pyld import jsonld
import pyld.documentloader.requests
import pandas as pd
import csv, os, json, copy


def deep_get(dikt, path):
    """Get a value or values located in `path` from a nested dictionary.
    Use a string separated by periods as the path to access
    values in a nested dictionary:
    deep_get(data, "data.files.0") == data["data"]["files"][0]
    deep_get(data, "data.files") == data["data"]["files"][]
    """
    value = dikt
    for component in path.split("."):
        if component.isdigit():
            value = value[int(component)]
        elif type(value) == list:
            new = []
            for v in value:
                if component in v:
                    new.append(v[component])
            value = new
        else:
            if component in value:
                value = value[component]
    return value


def crosswalk_table(format_name):
    """Get frame from crosswalk table"""
    with open(os.path.dirname(__file__) + "/crosswalk.csv", newline="") as infile:
        frame = pd.read_csv(infile)
        frame.set_index("Property", inplace=True)
        subset = frame[[format_name]].copy()
        subset.rename(columns={format_name: "crosswalk"}, inplace=True)
        subset.dropna("index", inplace=True)
    return subset


def get_crosswalk_context(table):
    """Get context from frame"""
    crosswalk = {}
    # start with full codemeta context
    # url = 'https://doi.org/10.5063/schema/codemeta-2.0'
    # loader = jsonld.requests_document_loader()
    # context = loader(url)['document']['@context']
    # Then pull out parts that match with the crosswalk table
    infile = open(os.path.dirname(__file__) + "/codemeta_schema.jsonld", "r")
    context = json.load(infile)["@context"]
    crosswalk["schema"] = context["schema"]
    crosswalk["codemeta"] = context["codemeta"]
    for key in context.keys():
        if key in table.index:
            val = table.loc[key, "crosswalk"]
            if type(val) != str:
                for v in table.loc[key, "crosswalk"]:
                    crosswalk[v] = context[key]
            else:
                crosswalk[val] = context[key]
    return crosswalk


def add_bio_tools(json):
    """Add additional fields that require logic for bio.tools"""
    if "link" in json:
        for l in json["link"]:
            if l["type"] == "Repository":
                json["schema:codeRepository"] = {"@id": l["url"]}


def crosswalk(json, from_format, to_format="codemeta"):
    if to_format == "codemeta":
        #codemeta_context = "https://doi.org/10.5063/schema/codemeta-2.0"
        codemeta_context ='https://raw.githubusercontent.com/caltechlibrary/convert_codemeta/master/codemeta.jsonld'
        table = crosswalk_table(from_format)
        context = get_crosswalk_context(table)
        json["@context"] = context
        # Nested elements indicated by a . path need to be added manually
        for key in context.keys():
            if "." in key:
                json[context[key]["@id"]] = deep_get(json, key)
        #Elements from formats that need logic are added manually
        if from_format == "bio.tools":
            add_bio_tools(json)
        expanded = jsonld.expand(json)
        codemeta = jsonld.compact(expanded, codemeta_context)
        return codemeta
