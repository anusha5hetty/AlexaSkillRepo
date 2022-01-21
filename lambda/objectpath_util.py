import objectpath
import itertools
import types


def objectpath_parse_wrapper(appended_path, json_resp):
    result_types = (types.GeneratorType, itertools.chain)

    json_tree = objectpath.Tree(json_resp)
    result = json_tree.execute(appended_path)
    end_result = list(result) if isinstance(result, result_types) else [result]
    return end_result


def get_dct_containing_condition(key, value, json_resp):
    """
    returns list of dictionary which contains key value pair passed in the method
    """
    value = '"{}"'.format(value) if isinstance(value, str) else value

    obj_path_format = '$..*[@."{key}" is {value}]'
    obj_path = obj_path_format.format(key=key, value=value)

    records = objectpath_parse_wrapper(obj_path, json_resp)
    return records


def get_dct_containing_mul_conditions(json_resp, **conditions):
    """
    returns list of dictionary which contains key value pair passed in the method
    """
    conditions = _construct_filter_condition(**conditions)

    obj_path_format = '$..*[{conditions}]'
    obj_path = obj_path_format.format(conditions=conditions)

    records = objectpath_parse_wrapper(obj_path, json_resp)
    return records


def filter_dct_for_key(key, value, filter_key, json_resp):
    """
    returns list of values for filter key
    """
    value = '"{}"'.format(value) if isinstance(value, str) else value

    obj_path_format = '$..*[@."{key}" is {value}].."{filter_key}"'
    obj_path = obj_path_format.format(key=key, value=value, filter_key=filter_key)

    records = objectpath_parse_wrapper(obj_path, json_resp)
    return records


def filter_dct_for_multiple_keys(key, value, lst_filter_keys, json_resp):
    """
    returns list of dictionary with lst_filter_keys and values for the keys
    """
    str_filter_keys = '","'.join(lst_filter_keys)
    filter_key = str_filter_keys.replace('.', '"."')

    value = '"{}"'.format(value) if isinstance(value, str) else value

    obj_path_format = '$..*[@."{key}" is {value}].("{filter_key}")'
    obj_path = obj_path_format.format(key=key, value=value, filter_key=filter_key)

    records = objectpath_parse_wrapper(obj_path, json_resp)
    return records


def get_dct_value(dct_key, json_resp):
    appended_path = '$..{}'.format(dct_key)
    records = objectpath_parse_wrapper(appended_path, json_resp)
    return records


def _construct_filter_condition(**condition):
    where_clause = ''
    where_syntax = '(@."{key}" is {value}) '
    for key, value in condition.items():
        value = '"{}"'.format(value) if isinstance(value, str) else value

        temp_where = where_syntax.format(key=key, value=value)
        where_clause += 'and {}'.format(temp_where) if where_clause else temp_where
    return where_clause.strip()
