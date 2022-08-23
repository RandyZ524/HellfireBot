import re

import files
import misc

rarities = {'common': 1, 'rare': 2, 'epic': 3, 'heroic': 4}


def parse_boon(input: [str]) -> (str, str, int):
    input = [s.lower() for s in input]
    rarity = 'common'
    level = 1
    if input[len(input) - 1].isdigit():
        level = int(input[len(input) - 1])
        input = input[0: len(input) - 1]
    if input[len(input) - 1] in rarities.keys():
        rarity = input[len(input) - 1]
        input = input[0: len(input) - 1]
    boon_name = misc.fuzzy_boon(input)
    return boon_name, rarity, level


def parse_aspect(input: [str]) -> (str, int):
    input = [s.lower() for s in input]
    level = 5
    if input[len(input) - 1].isdigit():
        level = int(input[len(input) - 1])
        input = input[0: len(input) - 1]
    aspect_name = ' '.join(input)
    if aspect_name in files.aspects_info:
        return aspect_name, level
    if aspect_name in files.aspect_aliases and files.aspect_aliases[aspect_name] in files.aspects_info:
        return files.aspect_aliases[aspect_name], level
    return '', level


def parse_god(input: [str]) -> str:
    input = [s.lower() for s in input]
    god_name = ' '.join(input)
    if god_name in files.god_cores:
        return god_name
    if god_name in files.core_aliases and files.core_aliases[god_name] in files.god_cores:
        return files.core_aliases[god_name]
    return ' '


def parse_stat(stat_line: str, value: [float]) -> str:
    try:
        replace = re.findall(r'{.*}', stat_line)[0]
    except IndexError:
        return stat_line
    rounded = 's' not in replace and 'x' not in replace
    if len(value) == 2:
        value = f'{int(value[0] + 0.5)} - {int(value[1] + 0.5)}' if rounded \
            else f'{round(value[0], 2)} - {round(value[1], 2)}'
    else:
        value = int(value[0] + 0.5) if rounded else round(value[0], 2)
    if '+' in replace:
        value = f'+{value}'
    if '-' in replace:
        value = f'-{value}'
    if '%' in replace:
        value = f'{value}%'
    if 's' in replace:
        value = f'{value} Sec.'
    if 'x' in replace:
        value = f'{value}x'
    stat = re.sub(r'{.*}', f'**{value}**', stat_line)
    return stat