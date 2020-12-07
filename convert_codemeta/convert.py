from pyld import jsonld
import pyld.documentloader.requests
import pandas as pd
import csv, os, json, copy, requests


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


def put_path(components, value):
    """Recursive function to put value in component"""
    if len(components) > 1:
        new = components.pop(0)
        value = put_path(components, value)
    else:
        new = components[0]
    return {new: value}


def deep_put(dikt, path, value):
    """Put a value into a dikt in a structure described by a `path`.
    The 'path' is a string separated by periods.
    deep_put(data, "data.files", value) returns data["data"]["files"] = value
    """
    path_components = path.split(".")
    structure = put_path(path_components, value)
    for key in structure:
        if key in dikt:
            if isinstance(dikt[key], list):
                dikt[key].append(structure[key])
            else:
                existing = dikt.pop(key)
                dikt[key] = [existing, structure[key]]
        else:
            dikt.update(structure)
    return dikt


def crosswalk_table(format_name):
    """Get frame from crosswalk table"""
    with open(os.path.dirname(__file__) + "/crosswalk.csv", newline="") as infile:
        frame = pd.read_csv(infile)
        frame.set_index("Property", inplace=True)
        try:
            subset = frame[[format_name]].copy()
        except KeyError:
            print(
                f"""Format {format_name} is not available in the crosswalk.
            Available formats: {list(frame)}"""
            )
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


def add_zenodo(new_fields):
    """Add additional fields that require logic for zenodo"""
    if "contributors" in new_fields:
        contributors = new_fields["contributors"]
        if "Funder" in contributors:
            funding = contributors.pop("Funder")
            new_fields["contributors"] = [{"name": funding["name"], "type": "Funder"}]
    if "related_identifiers" in new_fields:
        formatted = []
        for item in new_fields["related_identifiers"]:
            for key, value in item.items():
                formatted.append({"relation": key, "identifier": value})
        new_fields["related_identifiers"] = formatted


def customize_zenodo(json):
    """Customize fields to match Zenodo format"""
    # Workaround for missing scope for title and name
    if "name" in json:
        name = json.pop("name")
        json["title"] = name
    if "creators" in json:
        creators = json["creators"]
        new = []
        for creator in creators:
            new_cre = {}
            if "@id" in creator:
                # Only support ORCID for now
                orcid = creator["@id"].split("https://orcid.org/")[1]
                new_cre["orcid"] = orcid
            if "affiliation" in creator:
                new_cre["affiliation"] = creator["affiliation"]
            if "schema:familyName" in creator:
                if "schema:givenName" in creator:
                    new_cre["name"] = (
                        creator["schema:familyName"]
                        + ", "
                        + creator["schema:givenName"]
                    )
                else:
                    new_cre["name"] = creator["schema:familyName"]
            new.append(new_cre)
        json["creators"] = new
    if "@type" in json:
        typev = json.pop("@type")
        if typev == "SoftwareSourceCode":
            json["upload_type"] = "software"
    if "schema:programmingLanguage" in json:
        json["keywords"].append(json.pop("schema:programmingLanguage"))
    if "codemeta:developmentStatus" in json:
        dev = json.pop("codemeta:developmentStatus")["@id"]
        json["keywords"].append("Development Status: " + dev)
    if "codemeta:maintainer" in json:
        # Don't know how to map
        json.pop("codemeta:maintainer")
    if "license" in json:
        # Need to confirm the license is available in Zenodo
        # This is an exact match - could be improved with fuzzy match
        license_api = "https://zenodo.org/api/licenses/?&size=1000"
        zenodo_data = requests.get(license_api).json()["hits"]["hits"]
        licenses = []
        for license in zenodo_data:
            licenses.append(license["id"])
        if json["license"] not in licenses:
            json.pop("license")


def crosswalk(json, from_format, to_format="codemeta"):
    if from_format == "codemeta":
        # codemeta_context = "https://doi.org/10.5063/schema/codemeta-2.0"
        from_context = "https://raw.githubusercontent.com/caltechlibrary/convert_codemeta/main/codemeta.jsonld"
    else:
        table = crosswalk_table(from_format)
        from_context = get_crosswalk_context(table)
        # Nested elements indicated by a . path need to be added manually
        for key in from_context.keys():
            if "." in key:
                context_key = from_context[key]["@id"]
                json[context_key] = deep_get(json, key)
    if to_format == "codemeta":
        # codemeta_context = "https://doi.org/10.5063/schema/codemeta-2.0"
        to_context = "https://raw.githubusercontent.com/caltechlibrary/convert_codemeta/main/codemeta.jsonld"
    else:
        table = crosswalk_table(to_format)
        to_context = get_crosswalk_context(table)
        new_fields = {}
        # Nested elements indicated by a . path need to be added manually
        for key in to_context.keys():
            if "." in key:
                context_key = to_context[key]["@id"].split(":")[1]
                if context_key in json:
                    value = json[context_key]
                    deep_put(new_fields, key, value)
                    # We don't need the old value
                    json.pop(context_key)
    json["@context"] = from_context
    # Elements from formats that need logic are added manually
    if from_format == "bio.tools":
        add_bio_tools(json)
    if to_format == "Zenodo":
        add_zenodo(new_fields)
    expanded = jsonld.expand(json.copy())
    codemeta = jsonld.compact(expanded, to_context)
    if to_format == "Zenodo":
        customize_zenodo(codemeta)
    if to_format != "codemeta":
        # Context not appropriate for non-ld formats
        codemeta.pop("@context")
        # Add in non-codemeta fields
        codemeta.update(new_fields)

    return codemeta
