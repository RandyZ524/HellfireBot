import files
import parsing

rarity_graph_colors = ['#7D7D7D', '#0083F3', '#9500F6', '#FF1C10', '#FFD511']
rarity_embed_colors = [0xFFFFFF, 0x0083F3, 0x9500F6, 0xFF1C10, 0xFFD511, 0xD1FF18]
god_colors = {'zeus': 0xFCF75B, 'poseidon': 0x4AC4FB, 'athena': 0xF8C741, 'aphrodite': 0xFB91FC,
              'artemis': 0xD2FC61, 'ares': 0xFB2A2D, 'dionysus': 0xD111DE, 'demeter': 0xECFBFC,
              'hermes': 0xFBF7A7, 'bouldy': 0x3D4E46, 'duos': 0xD1FF18, 'hades': 0x9500F6, 'chaos': 0x8783CF}
god_icons = {'zeus': 'https://cdn.discordapp.com/emojis/1007940434129064019.webp?size=96&quality=lossless',
             'poseidon': 'https://cdn.discordapp.com/emojis/1007940611850125393.webp?size=96&quality=lossless',
             'athena': 'https://cdn.discordapp.com/emojis/1007940470627893338.webp?size=96&quality=lossless',
             'aphrodite': 'https://cdn.discordapp.com/emojis/1007940684231217173.webp?size=96&quality=lossless',
             'artemis': 'https://cdn.discordapp.com/emojis/1007940543403262033.webp?size=96&quality=lossless',
             'ares': 'https://cdn.discordapp.com/emojis/1007940354873507880.webp?size=96&quality=lossless',
             'dionysus': 'https://cdn.discordapp.com/emojis/1007940646373425182.webp?size=96&quality=lossless',
             'demeter': 'https://cdn.discordapp.com/emojis/1007940575674241055.webp?size=96&quality=lossless',
             'hermes': 'https://cdn.discordapp.com/emojis/1007940503179898990.webp?size=96&quality=lossless',
             'bouldy': 'https://cdn.discordapp.com/emojis/1014438782755422220.webp?size=96&quality=lossless',
             'chaos': 'https://cdn.discordapp.com/emojis/1015394974088573038.webp?size=96&quality=lossless'}
weapon_icons = {'sword': 'https://cdn.discordapp.com/emojis/1016977627485057034.webp?size=96&quality=lossless',
                'spear': 'https://cdn.discordapp.com/emojis/1016977626201587763.webp?size=96&quality=lossless',
                'shield': 'https://cdn.discordapp.com/emojis/1016977625081712660.webp?size=96&quality=lossless',
                'bow': 'https://cdn.discordapp.com/emojis/1016977619956277279.webp?size=96&quality=lossless',
                'fists': 'https://cdn.discordapp.com/emojis/1016977621705314315.webp?size=96&quality=lossless',
                'rail': 'https://cdn.discordapp.com/emojis/1016977623349469204.webp?size=96&quality=lossless'}


def fuzzy_boon(input: [str]) -> str:
    boon_name = ' '.join(input)
    if boon_name in files.boons_info:
        return boon_name
    if boon_name in files.misc_aliases and files.misc_aliases[boon_name] in files.boons_info:
        return files.misc_aliases[boon_name]
    for index, word in enumerate(input):
        if word in files.core_aliases:
            input[index] = files.core_aliases[word]
    if len(input) >= 2:
        if input[0] in files.god_cores.keys() and input[1] in files.god_cores[input[0]].keys():
            return files.god_cores[input[0]][input[1]]
        if input[1] in files.god_cores.keys() and input[0] in files.god_cores[input[1]].keys():
            return files.god_cores[input[1]][input[0]]
    if ' '.join(input) in files.boons_info:
        return ' '.join(input)
    return ''


def adjust_boon_type(info: {}, boon_name: str, rarity: str, level: int) -> (str, str, int):
    if info['type'] in ['legendary', 'duo']:
        output = f'**{info["type"].upper()}** {boon_name.upper()}\n'
        rarity = 'common'
        level = 1
    else:
        if len(info['rarities']) == 3 and rarity == 'heroic':
            rarity = 'epic'
        if info['levels'][0] == '0':
            output = f'**{rarity.upper()}** {boon_name.upper()}\n'
            level = 1
        else:
            output = f'**{rarity.upper()}** {boon_name.upper()} LV.{level}\n'
    return output, rarity, level


def boon_value(info: {str: str}, rarity: str) -> [float]:
    value = [float(x) for x in info['rarities'][parsing.rarities[rarity] - 1].split('-')]
    if rarity != 'common':
        if len(value) == 2 or info['god'] == 'chaos':
            base_value = info['rarities'][0].split('-')
            value = [float(base_value[0]) * value[0], float(base_value[-1]) * value[-1]]
    return value


def rarity_rolls(*args) -> [float]:
    def buff_rolls(buffs: [float]) -> None:
        for i in range(len(buffs)):
            rolls[i] += buffs[i]

    rolls = [0.12, 0.05, 0.1]
    if 'miniboss' in args:
        rolls = [0.1, 0.25, 1]
    elif 'hermes' in args:
        rolls = [0.01, 0.03, 0.06]
    elif 'chaos' in args:
        rolls = [0.01, 0.05, 0.1]
        if 'egg' in args:
            buff_rolls([0.1, 0.15, 0.4])
    if 'keepsake' in args:
        buff_rolls([0.1, 0.1, 0.2])
    if 'favor' in args:
        buff_rolls([0.1, 0.1, 0.2])
    if 'yarn' in args or 'nectar' in args:
        buff_rolls([0.1, 0.25, 1])
    if 'exclusive' in args:
        buff_rolls([0, 1, 0])
    if 'olympian' in args:
        buff_rolls([0, 0, 0.4])
    if 'pride' in args:
        buff_rolls([0, 0.2, 0])
    elif 'legacy' in args:
        buff_rolls([0.1, 0, 0])
    return rolls


def capwords(s: str) -> str:
    output = ' '.join((x[0].upper() + x[1:] if x.lower() not in ['of', 'the'] else x.lower()) for x in s.split(' '))
    if '-' in output:
        dash = output.index('-')
        output = output[:dash] + '-' + output[dash + 1].upper() + output[dash + 2:]
    return output
