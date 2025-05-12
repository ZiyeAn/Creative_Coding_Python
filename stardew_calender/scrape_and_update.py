import requests
from bs4 import BeautifulSoup
import os
import json
import time

# Store as json
def save_json(data, filename):
    os.makedirs("data", exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f" Saved to {filename}")


def get_loved_gifts(npc_name):
    url = f"https://stardewvalleywiki.com/{npc_name.replace(' ', '_')}"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    gifts = []

    for row in soup.select("table#infoboxtable tr"):
        section = row.find("td", id="infoboxsection")
        detail = row.find("td", id="infoboxdetail")
        if not section or not detail:
            continue

        if "loved gifts" in section.text.strip().lower():
            gifts = [a.text.strip() for a in detail.select("span.nametemplate a") if a.text.strip()]
            break

    return gifts
    
# birthday
def scrape_birthdays():
    url = "https://stardewvalleywiki.com/Calendar#Birthdays"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    tables = soup.select("table.wikitable")
    birthday_tables = [tables[2], tables[5], tables[8], tables[10]] 
    seasons = ["spring", "summer", "fall", "winter"]

    birthday_data = {season: [] for season in seasons}

    for season, table in zip(seasons, birthday_tables):
        for row in table.select("tr")[1:]:
            cols = row.select("td")
            if len(cols) >= 2:
                date = cols[0].text.strip().replace("th", "").replace("st", "").replace("nd", "").replace("rd", "")
                name = cols[1].text.strip()

                print(f"fetch {name} loved-gifts'...")
                loved_gifts = get_loved_gifts(name)
                print(f"{name}: {loved_gifts}")
                birthday_data[season].append({
                    "date": date,
                    "name": name,
                    "loved_gifts": loved_gifts
                })

    return birthday_data


# festivals
def scrape_festivals():
    url = "https://stardewvalleywiki.com/Calendar"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    tables = soup.select("table.wikitable")
    festival_tables = [tables[0], tables[3], tables[6], tables[9]]  # 春、夏、秋、冬
    seasons = ["spring", "summer", "fall", "winter"]

    fest_data = {season: [] for season in seasons}

    for season, table in zip(seasons, festival_tables):
        rows = table.select("tr")[1:]  # 跳过表头
        for row in rows:
            cols = row.select("td")
            if len(cols) >= 2:
                date = cols[0].text.strip().replace("th", "").replace("st", "").replace("nd", "").replace("rd", "")
                name = cols[1].text.strip()
                fest_data[season].append({
                    "date": date,
                    "name": name
                })
    return fest_data


# crops
def get_crop_details(href):
    url = f"https://stardewvalleywiki.com{href}"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    grow_days = None
    price = None

    for section in soup.find_all("td", id="infoboxsection"):
        title = section.text.strip().lower()
        value_td = section.find_next_sibling("td", id="infoboxdetail")
        if not value_td:
            continue
        value = value_td.text.strip().split()[0].replace("g", "").replace(",", "")
        if "growth time" in title:
            try:
                grow_days = int(value)
            except:
                pass
        elif "sell price" in title:
            try:
                price = int(value)
            except:
                pass

        if grow_days and price:
            break

    return grow_days, price

def scrape_crops():
    url = "https://stardewvalleywiki.com/Crops"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    crops_by_season = {
        "spring": [],
        "summer": [],
        "fall": []
    }

    tbody = soup.select("tbody")[-1]
    season = None

    for row in tbody.find_all("tr"):
        th = row.find("th")
        td = row.find("td")

        if th and th.find("a"):
            title = th.find("a").get("title", "").lower()
            if title in crops_by_season:
                season = title

        if not season or not td:
            continue

        for a in td.find_all("a"):
            name = a.text.strip()
            href = a.get("href", "")
            if name and href:
                if name in [c["name"] for c in crops_by_season[season]]:
                    continue
                print(f" Fetching {name}...")
                grow_days, price = get_crop_details(href)
                crops_by_season[season].append({
                    "name": name,
                    "grow_days": grow_days,
                    "price": price
                })
                time.sleep(0.5)  

    return crops_by_season

# scrape and store
def update_all():
    print("scrape birthday...")
    birthdays = scrape_birthdays()
    save_json(birthdays, "data/birthdays.json")

    print("scrape festivals...")
    festivals = scrape_festivals()
    save_json(festivals, "data/festivals.json")

    print("scrape crops...")
    crops = scrape_crops()
    save_json(crops, "data/crops.json")

    print("All stored")

if __name__ == "__main__":
    update_all()