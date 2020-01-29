import pytest
import os
import sys
import json

sys.path.append(os.getcwd())
sys.path.append('../')

from .. import const
from .. import json_key_list

BASE_NAME = const.BASE_NAME
LIST_INDEX_NAME = const.LIST_INDEX_NAME
JSON_SEP = const.JSON_SEP
DROP_VALUE_MAP = const.DROP_VALUE_MAP

EXPECT_DIR = 'expect'
INPUT_DIR = 'input'
SEP = ': '


def read_expect(expect_path):
    with open(expect_path, 'r') as f:
        # lines = f.readlines()
        lines = f.read().splitlines()
        expect_map = dict()
        for item in lines:
            tmp_line = str(item)
            sep_index = tmp_line.find(SEP)
            expect_map[tmp_line[:sep_index]] = tmp_line[sep_index + len(SEP):]
    return expect_map


def read_input(input_path):
    with open(input_path, 'r') as f:
        json_dict = json.load(f)
    return json_dict


@pytest.mark.parametrize('input_json, drop, expect', [
    ('sample_min.json', False, 'sample_min_default.txt'),
    ('sample_min.json', True, 'sample_min_drop.txt'),
    ('sample.json', True, 'sample_drop.txt'),
])
def test_basic_usage(input_json, drop, expect):
    input_json_path = os.path.join(INPUT_DIR, input_json)
    expect_path = os.path.join(EXPECT_DIR, expect)
    test_json = read_input(input_json_path)
    expect_map = read_expect(expect_path)

    line_map = dict()
    json_key_list.json2line(test_json, line_map, drop=drop)

    for key in line_map.keys():
        assert str(line_map[key]) == expect_map[key].replace('\"', '')
