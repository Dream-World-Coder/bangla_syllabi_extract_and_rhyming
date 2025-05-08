from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup, NavigableString
import time, os

BASE_URL = "https://www.bangla-kobita.com"
OUTPUT_FILE = os.path.join(os.getcwd(), "database", "passage.txt")

# Selenium setup (headless)
opts = Options()
opts.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)

def make_soup(url, wait=2):
    driver.get(url)
    time.sleep(wait)
    return BeautifulSoup(driver.page_source, "html.parser")

def get_poem_text(soup):
    title = soup.find("h1")
    if not title:
        return None
    lines = []
    for sib in title.next_siblings:
        # stop when we reach the next <h2> (i.e. “## প্রাসঙ্গিক Related”)
        if getattr(sib, "name", None) == "h2":
            break
        # collect text nodes and <br/> tags
        if isinstance(sib, NavigableString):
            text = sib.strip()
            if text:
                lines.append(text)
        elif sib.name == "br":
            lines.append("\n")
        else:
            txt = sib.get_text(separator="\n").strip()
            if txt:
                lines.append(txt)
    return "\n".join(lines).strip()


# 1) load main page, grab poets
main_soup = make_soup(BASE_URL)
poets = []
for a in main_soup.select('ul.item-list li[itemtype="https://schema.org/Person"] a'):
    href = a["href"]
    url = href if href.startswith("http") else BASE_URL + href
    poets.append((a.get_text(strip=True), url))

# 2) for each poet, fetch their poem list
with open(OUTPUT_FILE, "a", encoding="utf-8") as fout:
    for poet_name, poet_url in poets:
        print(f"Scraping {poet_name}")
        poet_soup = make_soup(poet_url)
        rows = poet_soup.select('#poem table tbody tr')
        for row in rows:
            link = row.select_one('td:nth-of-type(3) > a')
            if not link:
                continue
            title = link.get_text(strip=True)
            href = link["href"]
            poem_url = href if href.startswith("http") else BASE_URL + href
            print(" →", title)
            poem_soup = make_soup(poem_url)
            text = get_poem_text(poem_soup)
            if not text:
                print("    (still no content!)")
                continue
            fout.write(f"=== {poet_name} — {title} ===\n")
            fout.write(text + "\n\n")
            time.sleep(1)

driver.quit()
print("Done. Poems saved to", OUTPUT_FILE)
