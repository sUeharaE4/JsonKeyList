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

EXPECT_DIR = os.path.join(os.path.dirname(__file__), 'expect')
INPUT_DIR = os.path.join(os.path.dirname(__file__), 'input')
SEP = ': '


def read_expect(expect_path, sep):
    """
    期待値のtxtから改行を除いてdictを生成する.

    Parameters
    ----------
    expect_path : str
        期待値のPath.
    sep : str
        txtの1行をkey-valueに分割する区切り文字.

    Returns
    -------
    expect_map : dict
        txtを1行ずつkey-value形式で取得したdict.
    """
    with open(expect_path, 'r') as f:
        # lines = f.readlines()
        lines = f.read().splitlines()
        expect_map = dict()
        for item in lines:
            tmp_line = str(item)
            sep_index = tmp_line.find(sep)
            expect_map[tmp_line[:sep_index]] = tmp_line[sep_index + len(sep):]
    return expect_map


def read_input(input_path):
    """
    テスト対象のJSONを読み込みdictを生成する.

    Parameters
    ----------
    input_path : str
        テスト対象のJSONファイルPath.

    Returns
    -------
    json_dict : dict
        JSONを読み込み生成したdict.
    """
    with open(input_path, 'r') as f:
        json_dict = json.load(f)
    return json_dict


def __compare_util(input_json, expect, drop, base_name=None, remove_base=False):
    """
    テスト対象と期待値のファイルを読み込み、変換結果と比較するUtility.

    Parameters
    ----------
    input_json : str
        テスト対象のJSONファイル名.
    expect : str
        期待値のファイル名.
    drop : bool
        json2line実行時にvalueが配列やObjectの場合値を捨てるか.
    base_name : str
        JsonPathの一番はじめの値(Noneの場合はデフォルト。削除はしない).
    remove_base : bool
        JSON加工時に追加したroot_keyを削除するか否か.
    """
    input_json_path = os.path.join(INPUT_DIR, input_json)
    expect_path = os.path.join(EXPECT_DIR, expect)
    test_json = read_input(input_json_path)
    expect_map = read_expect(expect_path, SEP)

    line_map = dict()
    if base_name is None:
        json_key_list.json2line(test_json, line_map, drop=drop)
        base_name = BASE_NAME
    else:
        json_key_list.json2line(test_json, line_map, drop=drop, current_key=base_name)

    if remove_base:
        line_map = json_key_list.remove_base_name(line_map, base_name)

    for key in line_map.keys():
        assert str(line_map[key]) == expect_map[key].replace('\"', '')


@pytest.mark.parametrize('input_json, drop, expect', [
    ('sample_min.json', False, 'sample_min_default.txt'),
    ('sample_min.json', True, 'sample_min_drop.txt'),
    ('sample.json', True, 'sample_drop.txt'),
])
def test_basic_usage(input_json, drop, expect):
    __compare_util(input_json, expect, drop)


def test_change_name():
    __compare_util('sample_min.json', 'sample_min_change_name.txt', False, 'OBJ')


@pytest.mark.parametrize('input_json, drop, expect', [
    ('sample_min.json', False, 'sample_min_default_remove_base.txt'),
    ('sample_min.json', True, 'sample_min_drop_remove_base.txt'),
    ('sample.json', True, 'sample_drop_remove_base.txt'),
])
def test_remove_base_name(input_json, drop, expect):
    __compare_util(input_json, expect, drop=drop, remove_base=True)

