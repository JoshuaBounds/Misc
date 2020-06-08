
import re


def dynamic_padding(item, index, trigger_pattern=r'#+'):
    searches = re.finditer(trigger_pattern, item)
    string_array = list(item)
    for search in searches:
        insert = '{:0{}}'.format(index, search.end() - search.start())
        string_array[search.start():search.end()] = list(insert)
    return ''.join(string_array)


def dynamic_padding2(item, index, trigger_pattern=r'#+'):
    re_trigger = re.compile(trigger_pattern)
    searches = re_trigger.finditer(item)
    subbed = re_trigger.sub('{:0{}}', item)
    return subbed.format(*sum(
        ((index, search.end() - search.start()) for search in searches),
        tuple()
    ))


if __name__ == '__main__':

    print(dynamic_padding2('time ## thing #### bob', 1))
