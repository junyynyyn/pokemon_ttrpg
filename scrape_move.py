from bs4 import BeautifulSoup
import urllib.request

def scrape_move(move_name: str):
    # Scrape move from serebii database
    # Get Attack Name
    # Get type
    # Get category (physical, special, status)
    # Get PP and convert to PP consumption
    # Get move power, convert to dice
    # 10-25 1d4
    # 30-45 2d4
    # 50-65 3d6
    # 70-85 4d6
    # 90-105 5d8
    # 110-125 5d10
    # 130-145 5d12
    # 150 6d12
    # Get accuracy, convert to accuracy modifier