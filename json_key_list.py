import const

json_path = 'sample_min.json'

BASE_NAME = const.BASE_NAME
LIST_INDEX_NAME = const.LIST_INDEX_NAME
JSON_SEP = const.JSON_SEP
DROP_VALUE_MAP = const.DROP_VALUE_MAP


def remove_base_name(line_map, base_name=BASE_NAME):
    """
    JSON加工時に追加したroot_keyを削除する.

    Parameters
    ----------
    line_map : dict
        加工済みの辞書.
    base_name : str
        root_key文字列(base_name + '.'が削除される.

    Returns
    -------
    removed_map : dict
        root_keyを削除した辞書
    """
    removed_map = dict()
    for key in line_map:
        new_key = key[len(base_name + '.'):]
        removed_map[new_key] = line_map[key]
    return removed_map


def json2line(json_dict, line_map, current_key=BASE_NAME, drop=False):
    """
    JSONのkeyをドットでつないだ形式に変換する.

    Parameters
    ----------
    json_dict : dict
        JSONを読み込んだ辞書(またはその一部).
    line_map : dict
        ドットでつないだ形式でデータを保持する辞書.
    current_key : str
        現在処理しているkey
    drop : bool
        valueがobject, list だった場合、値を保持しない場合はTrue
    -------
    """
    base_key = current_key
    for key, value in json_dict.items():
        current_key = current_key + JSON_SEP + key
        __filtering_obj_value(value, line_map, current_key, drop)
        current_key = base_key


def __mapping_line(line_value, line_map, drop,
                   current_key=BASE_NAME, list_index=0):
    """
    JSON読み込み中のlist形式データを辞書に登録する.

    Parameters
    ----------
    line_value : list
        JSON の list形式データ
    line_map : dict
        ドットでつないだ形式でデータを保持する辞書.
    drop : bool
        valueがobject, list だった場合、値を保持しない場合はTrue
    current_key : str
        現在処理しているkey
    list_index : int
        list形式データの現在処理しているindex
    """
    base_key = current_key
    for value in line_value:
        current_key = current_key + JSON_SEP + \
                      LIST_INDEX_NAME.format(index=list_index)
        __filtering_line_value(value, line_map, current_key, drop)
        current_key = base_key
        list_index = list_index + 1


def __decide_value(value, value_type, drop):
    """
    値を保持するかどうかに応じて値を決定するUtility.

    Parameters
    ----------
    value : object
        JsonPathに応じたValue
    value_type : str
        valueの型。返却する値を設定するために使用する.
    drop : bool
        valueがobject, list だった場合、値を保持しない場合はTrue

    Returns
    -------
    value : object
        値を保持する場合はそのまま。削除する場合はobject->{},list->[]
    """
    if drop:
        return DROP_VALUE_MAP[value_type]
    return value


def __filtering_obj_value(value, line_map, current_key, drop):
    """
    JSON の object をマッピングするためのUtility.

    Parameters
    ----------
    value : object
        JsonPathに応じたValue.
    line_map : dict
        ドットでつないだ形式でデータを保持する辞書.
    current_key : str
        現在処理しているkey
    drop : bool
        valueがobject, list だった場合、値を保持しない場合はTrue
    """
    if type(value) == dict:
        line_map[current_key] = __decide_value(value, 'dict', drop)
        json2line(value, line_map, current_key, drop)
    elif type(value) == list:
        line_map[current_key] = __decide_value(value, 'list', drop)
        __mapping_line(value, line_map, drop, current_key)
    else:
        line_map[current_key] = value


def __filtering_line_value(value, line_map, current_key, drop):
    """
    JSON の list をマッピングするためのUtility.

    Parameters
    ----------
    value : object
        JsonPathに応じたValue.
    line_map : dict
        ドットでつないだ形式でデータを保持する辞書.
    current_key : str
        現在処理しているkey
    drop : bool
        valueがobject, list だった場合、値を保持しない場合はTrue
    """
    if type(value) == dict:
        line_map[current_key] = __decide_value(value, 'dict', drop)
        json2line(value, line_map, current_key, drop)
    elif type(value) == list:
        line_map[current_key] = __decide_value(value, 'list', drop)
        __mapping_line(value, line_map, drop, current_key)
    else:
        line_map[current_key] = value
