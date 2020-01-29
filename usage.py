import json
from json_key_list import json2line, remove_base_name
import const


json_path = 'sample_min.json'
base_name = 'base_name'


def create_line_map(input_json, drop=False):
    line_map = dict()
    json2line(input_json, line_map)
    return line_map


def create_line_map_without_base_name(input_json, drop=False):
    line_map = dict()
    json2line(input_json, line_map)
    return remove_base_name(line_map, const.BASE_NAME)


def print_keys(dict_):
    for key in dict_:
        print(key)


def print_key_values(dict_):
    for key in dict_:
        print(str(key) + ': ' + str(dict_[key]))

with open(json_path) as f:
    input_json = json.load(f)

print('###### change base_name ######')
line_map = dict()
json2line(input_json, line_map, base_name)
print_keys(line_map)

print('###### remove base_name (show value) ######')
line_map = dict()
json2line(input_json, line_map)
removed_map = remove_base_name(line_map)
print_key_values(removed_map)

print('###### remove base_name and drop value when data type is object or list (show value) ######')
line_map = dict()
json2line(input_json, line_map, drop=True)
removed_map = remove_base_name(line_map)
print_key_values(removed_map)

