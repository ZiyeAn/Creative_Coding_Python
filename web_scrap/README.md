# 🌾 Stardew Valley Web Scraper

This project scrapes character data from the [Stardew Valley Wiki - Villagers Page](https://stardewvalleywiki.com/Villagers).

[Click to View Code](main.py)

## 🔍 What It Does

1. Scrapes the following from the main villagers page:
   - Character **names**
   - **Image URLs**
   - **Links** to their individual character pages
   - **A short info** of individuals in their individual character pages
2. Visits each character's page to scrape additional **detailed info** (like quotes).
3. Saves all collected data into a CSV file.

<img src="images/Screenshot 2025-03-30 at 4.52.18 PM.png">
---

## 🔁 Iterations & Fixes

### 🧩 Problem 1: SSL Certificate Error

**Error:**  

urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate

**Reason:**  
Python was trying to securely connect to HTTPS image URLs, but my system didn’t have the required SSL certificates installed.

**Solution:**  
Run the following command to install the necessary certificates:
```bash
/Applications/Python\ 3.12/Install\ Certificates.command
```


⸻

### 🧩 Problem 2: 403 Forbidden Error While Downloading Images

Reason:
Websites often block requests that don’t appear to come from a real browser.

Solution:
Set a browser-like User-Agent in the header when downloading images:
```
import os
import urllib.request
from urllib.error import HTTPError, URLError

os.makedirs('images', exist_ok=True)  # Create folder for images
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

```

⸻

### 🧩 Problem 3: Using a Literal String in Requests

Mistake:
```
infoResponse = requests.get("https://stardewvalleywiki.com/{name}")
```
Reason:
This treats {name} as a literal string instead of using the actual variable.

Solution:
Use an f-string to insert the value of name into the URL:
```
url_name = name.replace(" ", "_")  # Adjust for wiki formatting
info_url = f"https://stardewvalleywiki.com/{url_name}"
infoResponse = requests.get(info_url)

```

⸻

### ✅ Final Output

All character data (name, image URL, link, quote) is saved into a final CSV file for further use.