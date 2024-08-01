from bs4 import BeautifulSoup
import urllib.request
import re

base_url = "https://serebii.net/attackdex-sv/"
url_end = ".shtml"

def scrape_move(move_name: str):
    # Remove spaces in move name
    move_name = re.sub(" ", "", move_name)
    move_name = move_name.lower()
    # # Scrape move from serebii database
    move = {}
    try:
        with urllib.request.urlopen(base_url + move_name + url_end) as response:
            html = response.read()
            soup = BeautifulSoup(html, 'html.parser')
            dextables = soup.find_all('table')

            attack_info = dextables[3].find_all('tr')
            # tr listing:
            # tr 1 contains attack name, type, category
            # tr 3 contains Max PP, Base Power, Accuracy
            # tr 5 contains battle description
            # tr 7 contains any secondary effects and their effect rate

            # Getting Attack Name
            attack_name = attack_info[1].find_all('td')[0].text
            # Using regex to remove non alphanumeric characters
            attack_name = re.sub('[^A-z1-9\-, ]', "", attack_name)
            move["attack_name"] = attack_name

            # Getting attack type
            attack_type = attack_info[1].find_all('td')[1].find('a')['href']
            # Using regex to remove start and end of typing
            attack_type = re.search('^/attackdex-sv\/(.*)\.shtml', attack_type).group(1).capitalize()
            move["type"] = attack_type

            # Getting attack category
            attack_category = attack_info[1].find_all('td')[2].find('a')['href']
            attack_category = re.search('^/attackdex-sv\/(.*)\.shtml', attack_category).group(1).capitalize()
            move["category"] = attack_category

            # Getting PP Max and converting to PP Usage
            pp_max = int(attack_info[3].find_all('td')[0].text.strip())
            pp_map = {40: 1, 35: 2, 30: 3, 25: 4, 20: 5, 15: 6, 10: 7, 5: 8}
            move["pp_usage"] = pp_map[pp_max]

            # Getting Move Power and converting to dice
            attack_power = attack_info[3].find_all('td')[1].text.strip()
            print(attack_power)
            # 10-25 1d4 avg 2
            # 30-45 2d4 avg 4
            # 50-65 2d6 avg 6
            # 70-85 3d6 avg 9
            # 90-105 3d8 avg 12
            # 110-125 4d8 avg 16
            # 130-145 4d10 avg 20
            # 150-160 5d10 avg 25
            # 180 5d12 avg avg 30
            # 200 6d12 avg 36
            # 250 7d12 avg 42
            power_thresholds = [25, 45, 65, 85, 105, 125, 145, 160, 180, 200, 250]
            power_map = ["1d4", "2d4", "3d6", "4d6", "5d8", "5d10", "5d12", "6d12", "8d12", "10d12", "12d12"]
            for i in range(len(power_thresholds)):
                if (int(attack_power) < power_thresholds[i]):
                    move["damage"] = power_map[i]
                    break

            # Getting move accuracy and converting to d20 roll
            attack_accuracy = attack_info[3].find_all('td')[2].text.strip()
            move["accuracy"] = int(int(attack_accuracy) / 5)

            print(move)
            
    except:
        print("Error while scraping page")
    # Get accuracy, convert to accuracy modifier
    return

if __name__ == "__main__":
    scrape_move("Fire Blast");