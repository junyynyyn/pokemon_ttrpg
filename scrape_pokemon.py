from bs4 import BeautifulSoup
import urllib.request
import re
import math

base_url = "https://serebii.net/pokedex-sv/"
url_end = ".shtml"


def scrape_pokemon_info(pokemon_name: str):
    # Scrape pokemon information off serebii
    pokemon = {}
    pokemon_name = re.sub(" ", "", pokemon_name)
    pokemon_name = pokemon_name.lower()
    try:
        with urllib.request.urlopen(base_url + pokemon_name + "/") as response:
            html = response.read()
            soup = BeautifulSoup(html, "html.parser")
            dextables = soup.find_all('table')
            # Dextable 3 = name
            # Dextable 7 = name, type, weight, capture rate
            # Dextable 11 = abilities
            # Dextable 15 = evolutions
            # Dextable 20 = level up moves
            # Dextable 21 = Technical Machines
            # Dextable 22 = Egg Moves
            # Dextable 23 = Stats
            pokemon["stats"] = parse_pokemon_stats(dextables[23])
    except:
        return


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
    # Parse pokemon moves learnt by level
    pass

def parse_pokemon_tm_moves(pokemon_info):
    # Parse pkoemon moves learnt by TM
    pass

def ttrpg_base_stats(pokemon_info):
    # Convert official game stats to TTRPG Stats
    pass

def ttrpg_level_moves(pokemon_info):
    # Convert official game levels learnt into TTRPG levels learnt
    pass

def ttrpg_tm_moves(pokemon_info):
    # Npt really required
    pass

def ttrpg_catch_rate(pokemon_info):
    # Parse and convert catch rate of pokemon into TTRPG Catch rating
    pass

def get_types(pokemon_info):
    # Get type(s) of the pokemon
    pass

def ttrpg_weight(pokemon_info):
    # Get weight and convert to ttrpg weight through binning
    pass

def get_abilities(pokemon_info):
    # Get ability list of the pokemon
    pass

def compile_ttrpg_info(pokemon_name: str):
    # Compile info about the pokemon and return it in json format
    pass


if __name__ == "__main__":
    scrape_pokemon_info("bulbasaur")