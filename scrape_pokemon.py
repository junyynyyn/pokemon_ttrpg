from bs4 import BeautifulSoup
import urllib.request

def scrape_pokemon_info(pokemon_name: str):
    # Scrape pokemon information off serebii
    pass

def parse_pokemon_stats(pokemon_info):
    # Parse pokemon base stats 
    pass

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




page = urllib.request.urlopen("")