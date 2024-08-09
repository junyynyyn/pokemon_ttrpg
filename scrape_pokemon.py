from bs4 import BeautifulSoup
import urllib.request
import re
import math
import json

base_url = "https://serebii.net/pokedex-sv/"
url_end = ".shtml"


def scrape_pokemon_info(pokemon_name: str):
    # Scrape pokemon information off serebii
    pokemon_name = re.sub(" ", "", pokemon_name)
    pokemon_name = pokemon_name.lower()
    try:
        with urllib.request.urlopen(base_url + pokemon_name + "/") as response:
            html = response.read()
            soup = BeautifulSoup(html, "html.parser")
            return soup
    except:
        return

def get_table_title(table):
    header = ''
    if (table.find('h3')):
        header = table.find('h3').text
    elif (table.find('h2')):
        header = table.find('h2').text
    elif (table.find('b')):
        header = table.find('b').text
    
    return header

def parse_info_table(soup_data):
    dextable = soup_data.find_all('table')[7]
    return dextable

def parse_move_tables(soup_data):
    tables = []
    for table in soup_data.find_all('table'):
        if (get_table_title(table) == "Standard Level Up" or get_table_title(table) == "Technical Machine Attacks"):
            tables.append(table)

    return tables

def parse_stats_table(soup_data):
    for table in soup_data.find_all('table'):
        if (get_table_title(table) == 'Stats'):
            return table

def parse_abilities_table(soup_data):
    for table in soup_data.find_all('table'):
        if (get_table_title(table) == 'Abilities'):
            return table

# Functions for parsing tables once extracted

def parse_pokemon_stats(pokemon_info):
    # Get pokemon base stats and convert them to TTRPG stats 
    # Divide by 10, round up for base stats
    # Multiply by 2 for HP
    base_stats = pokemon_info.find_all('tr')[2].find_all('td')
    stats = {}
    stats_names = ["HP", "Attack", "Defense", "Special Attack", "Special Defense", "Speed"]

    stats_list = list(map(lambda x: int(x.text), base_stats[1:]))

    ttrpg_stats = list(map(lambda x: math.ceil(x/10), stats_list))

    ttrpg_stats[0] *= 2
    
    for i in range(len(ttrpg_stats)):
        stats[stats_names[i]] = ttrpg_stats[i]

    return stats

def parse_pokemon_level_moves(pokemon_info):
    # Return a dictionary of moves by levels 1-20
    # Pokemon learn levels are their game levels / 5 rounded down
    # E.g. {1: ["Tackle, Leech Seed"], 2: ["Fire Blast"]}

    # Parse Level values into array
    levels_soup = pokemon_info.find_all('td', class_="fooinfo",text=re.compile('^(\d{1,3}|—|Evolve)$'))
    # levels = [x.text for x in levels_soup]
    levels = list(map(lambda x: 1 if x.text == "—" or x.text == "Evolve" else int(x.text), levels_soup))
    # Parse Move Names into array
    moves_soup = pokemon_info.find_all('a',text=re.compile('\w+'))
    moves = [x.text for x in moves_soup]

    level_moves = {}

    for i in range(len(moves)):
        ttrpg_level = math.ceil(levels[i] / 5)
        if (ttrpg_level not in level_moves.keys()):
            level_moves[ttrpg_level] = [moves[i]]
        else:
            level_moves[ttrpg_level].append(moves[i])
    
    return level_moves

def parse_pokemon_tm_moves(pokemon_info):
    moves_soup = pokemon_info.find_all('a',text=re.compile('\w+'))
    moves = [x.text for x in moves_soup if "TM" not in x.text]
    
    return moves

def parse_catch_rate(pokemon_info):
    # Parse and convert catch rate of pokemon into TTRPG Catch rating
    catch_rate = int(pokemon_info.find(class_='fooinfo',text=re.compile('\d{1,3}')).text)

    return ttrpg_catch_rate(catch_rate)

def ttrpg_catch_rate(rate): 
    return rate

def parse_types(pokemon_info):
    types = []
    types_img = pokemon_info.find_all('img')
    for i in range(0, len(types_img)):
        typing = re.search('^(.*)\-type', types_img[i]['alt']).group(1).capitalize()
        types.append(typing)   
    return types

def parse_weight(pokemon_info):
    weights = ["Featherweight", "Light", "Medium", "Heavy", "Very Heavy", "Very Heavy"]
    weight_thresholds = [21.8, 54.9, 109.8, 220.2, 438.7, 2204.4]
    # Get weight and convert to ttrpg weight through binning

    weight = pokemon_info.find(text=re.compile('lbs'))
    weight_float = float(re.search('^(\d*\.\d*)lbs', weight).group(1))
    for i in range(len(weight_thresholds)):
        if (weight_float <= weight_thresholds[i]):
            return weights[i]
    return weights[len(weights)-1]

def parse_abilities(pokemon_info):
    abilities_a = pokemon_info.find_all('tr')[0].find_all('a')
    abilities = list(map(lambda x: x.text, abilities_a))
    
    return abilities

def parse_name(pokemon_info):
    return pokemon_info.find_all('td')[5].text

# Main Function
def compile_ttrpg_info(pokemon_name: str):
    # Compile info about the pokemon and return it in json format
    # Dextable 3 = name x
    # Dextable 7 = name, type, weight, capture rate
    # Dextable 11 = abilities x
    # Dextable 15 = evolutions
    # Dextable 20 = level up moves
    # Dextable 21 = Technical Machines
    # Dextable 22 = Egg Moves
    # Dextable 23 = Stats x
    pokemon = {}

    # Parse Data into Tables
    soup_data = scrape_pokemon_info(pokemon_name)
    info_table = parse_info_table(soup_data)
    move_tables = parse_move_tables(soup_data)
    stats_table = parse_stats_table(soup_data)
    abilities_table = parse_abilities_table(soup_data)

    pokemon["name"] = parse_name(info_table)
    pokemon["types"] = parse_types(info_table)
    pokemon["weight"] = parse_weight(info_table)
    pokemon["catch_rate"] = parse_catch_rate(info_table)

    pokemon["abilities"] = parse_abilities(abilities_table)

    pokemon["stats"] = parse_pokemon_stats(stats_table)
    pokemon["level_moves"] = parse_pokemon_level_moves(move_tables[0])
    pokemon["tm_moves"] = parse_pokemon_tm_moves(move_tables[1])
    return pokemon

if __name__ == "__main__":
    print(json.dumps(compile_ttrpg_info("arceus"), indent=4))