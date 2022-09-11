import misc

boons_info = {}
bouldy_info = []
charon_info = {}
aspects_info = {}
hammers_info = {}
keepsakes_info = {}
prereq_info = {}
aliases = {'core': {}, 'misc': {}, 'aspect': {}, 'hammer': {}, 'keepsake': {}}
god_cores = {'zeus': {}, 'poseidon': {}, 'athena': {}, 'aphrodite': {}, 'artemis': {}, 'ares': {},
             'dionysus': {}, 'demeter': {}, 'hermes': {}, 'chaos': {}, 'charon': {}, 'duos': None}

for god in god_cores:
    f = open(f'./files/gods/{god}.txt', 'r', encoding='utf8')
    while boon := f.readline().strip():
        type, boon = boon.split(' ', 1)
        has_prereq = type not in ('attack', 'special', 'cast', 'flare', 'dash', 'call',
                                  'revenge', 't1', 'blessing', 'curse', 'combat', 'survival',
                                  'spawning', 'resource', 'miscellaneous')
        if type[0] == 'x':
            type = type[1:]
        if type in ('attack', 'special', 'cast', 'flare', 'dash', 'call', 'status', 'revenge', 'legendary'):
            god_cores[god][type] = boon
        boons_info[boon] = {'god': god, 'type': type, 'desc': f.readline().strip(), 'stat': f.readline().strip(),
                            'rarities': f.readline().strip().split(' '), 'levels': f.readline().strip().split(' '),
                            'icon': f.readline().strip()}
        if has_prereq:
            prereqs = f.readline().strip().split('; ')
            prereq_list = []
            for prereq in prereqs:
                prereq_list.append((prereq[0], prereq[2: -1].split(', ')))
            prereq_info[boon] = prereq_list
        if type == 'call' and god not in ('hermes', 'charon'):
            boons_info[boon]['maxcall'] = f.readline().strip()
        if god == 'charon':
            boons_info[boon]['cost'] = f.readline().strip()
    f.close()

f = open('./files/gods/misc.txt', 'r', encoding='utf8')
while boon := f.readline().strip():
    god, type, boon = boon.split(' ', 2)
    has_prereq = False
    if type[0] == 'x':
        has_prereq = True
        type = type[1:]
    boons_info[boon] = {'god': god, 'type': type, 'desc': f.readline().strip(), 'stat': f.readline().strip(),
                        'rarities': f.readline().strip().split(' '), 'levels': f.readline().strip().split(' '),
                        'icon': f.readline().strip()}
    if has_prereq:
        prereqs = f.readline().strip().split('; ')
        prereq_list = []
        for prereq in prereqs:
            prereq_list.append((prereq[0], prereq[2: -1].split(', ')))
        prereq_info[boon] = prereq_list
    if type == 'call':
        boons_info[boon]['maxcall'] = f.readline().strip()
f.close()

f = open(f'./files/gods/bouldy.txt', 'r', encoding='utf8')
while f.readline():
    bouldy_info.append({'desc': f.readline().strip(), 'stat': f.readline().strip(), 'icon': f.readline().strip()})
f.close()

f = open('./files/aspects.txt', 'r', encoding='utf8')
while aspect := f.readline().strip():
    weapon, aspect = aspect.split(' ', 1)
    aspects_info[aspect] = {'weapon': weapon, 'desc': f.readline().strip(), 'stat': f.readline().strip(),
                            'levels': f.readline().strip().split(' '), 'flavor': f.readline().strip(),
                            'icon': f.readline().strip()}
f.close()

for weapon in misc.weapon_icons:
    f = open(f'./files/hammers/{weapon}.txt', 'r', encoding='utf8')
    while hammer := f.readline().strip():
        has_prereq = False
        if hammer[0] == 'x':
            has_prereq = True
            hammer = hammer[1:]
        hammers_info[hammer] = {'weapon': weapon, 'desc': f.readline().strip(), 'icon': f.readline().strip()}
        if has_prereq:
            prereqs = f.readline().strip().split('; ')
            prereq_list = []
            for prereq in prereqs:
                prereq_list.append((prereq[0], prereq[2: -1].split(', ')))
            prereq_info[hammer] = prereq_list
    f.close()

f = open('./files/keepsakes.txt', 'r', encoding='utf8')
while keepsake := f.readline().strip():
    type, keepsake = keepsake.split(' ', 1)
    keepsakes_info[keepsake] = {'type': type, 'desc': f.readline().strip(), 'ranks': f.readline().strip().split(' '),
                                'bond': f.readline().strip().rsplit(' ', 2), 'flavor': f.readline().strip(),
                                'icon': f.readline().strip()}
    if type != 'companion':
        for suffix in ('', ' keepsake', 's keepsake', '\' keepsake', '\'s keepsake'):
            aliases['keepsake'][keepsakes_info[keepsake]['bond'][0].lower() + suffix] = keepsake
    else:
        for suffix in (' companion', 's companion', '\' companion', '\'s companion', ' pet', 's pet', '\' pet', '\'s pet'):
            aliases['keepsake'][keepsakes_info[keepsake]['bond'][0].lower() + suffix] = keepsake
f.close()

for category in aliases:
    f = open(f'files/aliases/{category}aliases.txt', 'r', encoding='utf8')
    while name := f.readline().strip():
        alias_list = f.readline().strip().split(', ')
        if alias_list[0]:
            for alias in alias_list:
                if alias in aliases[category]:
                    print(f'duplicate alias: {alias}')
                aliases[category][alias] = name
    f.close()
