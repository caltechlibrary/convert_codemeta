from pyld import jsonld
import pyld.documentloader.requests
import pandas as pd
import csv, os, json


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
    for key in context.keys():
        if key in table.index:
            val = table.loc[key, "crosswalk"]
            if type(val) != str:
                for v in table.loc[key, "crosswalk"]:
                    crosswalk[v] = context[key]
            else:
                crosswalk[val] = context[key]
    return crosswalk


def crosswalk(json, from_format, to_format="codemeta", trim=True):
    if to_format == "codemeta":
        codemeta = "https://doi.org/10.5063/schema/codemeta-2.0"
        table = crosswalk_table(from_format)
        context = get_crosswalk_context(table)
        json["@context"] = context
        expanded = jsonld.expand(json)
        return jsonld.compact(expanded, codemeta)
