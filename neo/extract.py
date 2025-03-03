"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.

You'll edit this file in Task 2.
"""
import csv
import json

from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    # Load NEO data from the given CSV file.
    data=[]
    with open(neo_csv_path, 'r') as file:
        reader = csv.reader(file)
        for i, lines in enumerate(reader):
            if i==0:
                designation_index = lines.index('pdes')
                name_index = lines.index('name')
                pha_index = lines.index('pha')
                diameter_index = lines.index('diameter')
            else:
                data.append(NearEarthObject(
                    designation=lines[designation_index],
                    name=lines[name_index],
                    diameter=lines[diameter_index],
                    hazardous=True if lines[pha_index] == 'Y' else False
                ))
    return data


def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param cad_json_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    # Load close approach data from the given JSON file.

    cad=[]

    with open(cad_json_path, 'r') as file:
        data = json.load(file)
        des_index = data['fields'].index('des')
        cd_index = data['fields'].index('cd')
        dist_index = data['fields'].index('dist')
        v_rel_index = data['fields'].index('v_rel')
        for i in data['data']:
            cad.append(CloseApproach(time=i[cd_index],
                                    distance=i[dist_index],
                                    velocity=i[v_rel_index],
                                    designation=i[des_index]
                                    ))

    return cad