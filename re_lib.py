import re
import pandas as pd


def get_regex_groups(regex, data, group_names=None, flags=re.MULTILINE):
    """
    :param regex: regex to search pattern
    :param data: file content or string to be searched
    :param group_names: group names, as mentioned in the regex
    :param flags: re.finditer flags, default: re.MULTILINE
    :return: Returns a dictionary of key (group_index) and value (dictionary of group_name and search result)
    """
    matches = re.finditer(regex, data, flags=flags)
    result_dict = {}
    for matchNum, match in enumerate(matches):
        matches_dict = {}
        if group_names is None:
            for k, v in enumerate(match.groups()):
                matches_dict[k] = v
        else:
            for g in group_names:
                try:
                    matches_dict[g] = match.group(g)
                except:
                    matches_dict[g] = None
        result_dict[matchNum] = matches_dict
    return result_dict


def get_regex_groups_in_df(regex, data, group_names=None, flags=re.MULTILINE):
    result_dict = get_regex_groups(regex=regex, data=data, group_names=group_names, flags=flags)
    result_df = pd.DataFrame(result_dict)
    result_df = result_df.transpose()
    return result_df


def get_regex_groups_length(regex, data, group_names=None, flags=re.MULTILINE):
    result_dict = get_regex_groups(regex=regex, data=data, group_names=group_names, flags=flags)
    return len(result_dict)


def get_regex_match_num(regex, data, group_names=None, match_num=-1, flags=re.MULTILINE):
    result_dict = get_regex_groups(regex=regex, data=data, group_names=group_names, flags=flags)
    result_dict_keys = sorted(result_dict.keys())
    if match_num in result_dict_keys:
        return result_dict[match_num]
    else:
        max_key = max(result_dict_keys)
        return result_dict[max_key]


def get_regex_match_group(regex, data, group_name, match_num=-1, flags=re.MULTILINE):
    """
    :param regex: The parameter regex expects the regex pattern to be search
    :param data: The parameter data expects the file content or string to be searched
    :param group_name: The parameter group_name expects a single group name.
    If a list of string is provided, only the first group name would would be picked to search!
    Else return None
    :param match_num: The parameter match_num expects a single match_num. If not sent, it takes the last match.
    :param flags: re.finditer flags, default: re.MULTILINE
    :return: string with the search result
    """
    if isinstance(group_name, str):
        group_names = [group_name]
    elif isinstance(group_name, list):
        group_names = [group_name[0]]
    else:
        LOGGER.error("The parameter group name expects a single group name!")
        LOGGER.error("If a list of string is provided, only the first name would would be picked to search!")
        return None

    result_dict = get_regex_groups(regex=regex, data=data, group_names=group_names, flags=flags)
    result_dict_keys = sorted(result_dict.keys())

    if match_num in result_dict_keys:
        return result_dict[match_num]
    else:
        max_key = max(result_dict_keys)
        return result_dict[max_key]


def get_regex_match_str(regex, data, group_name=None, match_num=-1, flags=re.MULTILINE):
    """
    :param regex: The parameter regex expects the regex pattern to be search
    :param data: The parameter data expects the file content or string to be searched
    :param group_name: The parameter group_name expects a single group name.
    If a list of string is provided, only the first group name would would be picked to search!
    Else return None
    :param match_num: The parameter match_num expects a single match_num. If not sent, it takes the last match.
    :return: string with the search result
    """
    if isinstance(group_name, str):
        group = [group_name]
    elif isinstance(group_name, list):
        group = [group_name[0]]
    elif group_name is None:
        group = None
    else:
        LOGGER.error("The parameter group name expects a single group name!")
        LOGGER.error("If a list of string is provided, only the first name would would be picked to search!")
        return None

    result_dict = get_regex_groups(regex=regex, data=data, group_names=group, flags=flags)
    result_dict_keys = sorted(result_dict.keys())

    if len(result_dict_keys) > 0:
        try:
            if match_num in result_dict_keys:
                result = result_dict[match_num]
            else:
                max_key = max(result_dict_keys)
                result = result_dict[max_key]

            if group is None:
                return list(result.values())[0]
            else:
                return result[group[0]]
        except Exception as e:
            LOGGER.exception("Exception occurred :: {e}".format(e=e))
            return None
    else:
        LOGGER.warning("There was no match found!")
        return None
