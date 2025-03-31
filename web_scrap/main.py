import requests
import bs4
import pandas as pd
from itertools import product

response = requests.get("https://stardewvalleywiki.com/Villagers")
soup = bs4.BeautifulSoup(response.text, "html.parser")

names = []
imgs = []
links =[]
info = []


for item in soup.select(".gallerytext"):
    names.append(item.text.strip())

for img in soup.select('.thumb img'):
    img_url = img.get('src')
    # print(img_url)
    if img_url.startswith('//'):
        img_url = 'https:' + img_url
    elif img_url.startswith('/'):
        img_url = 'https://stardewvalleywiki.com' + img_url
    imgs.append(img_url)

for link in soup.select(".thumb a"):
    link_href = link.get("href")
    link_href = "https://stardewvalleywiki.com" + link_href
    links.append(link_href)

for name in names:
    url_name = name.replace(" ", "_")
    info_url = f"https://stardewvalleywiki.com/{url_name}"
    infoResponse = requests.get(info_url)
    infoSoup = bs4.BeautifulSoup(infoResponse.text, "html.parser")
    
    quotes = infoSoup.select(".quotetext")
    if quotes:
        info.append(quotes[0].text.strip())  
    else:
        info.append("No quote found")


length = min(len(names), len(imgs),len(links))
data = {
    'Name': names[:length],
    'Image_URL': imgs[:length],
    'Info':info[:length],
    'Links': links[:length],
}

df = pd.DataFrame(data)
df.to_csv('villagers3.0.csv', index=False)

import os
import urllib.request
from urllib.error import HTTPError, URLError

# Make sure the images folder exists
os.makedirs('images', exist_ok=True)

# Set a browser-like User-Agent
headers = {'User-Agent': 'Mozilla/5.0'}

for index, url in enumerate(imgs):
    file_name = f'img_{index}.jpg'
    full_path = os.path.join('images', file_name)
    print(file_name)

    req = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(req) as response:
            with open(full_path, 'wb') as f:
                f.write(response.read())
    except HTTPError as e:
        print(f'HTTPError for {url}: {e.code}')
    except URLError as e:
        print(f'URLError for {url}: {e.reason}')