from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup, NavigableString
import time, os

# ── Configuration ──────────────────────────────────────────────────────────────
BASE_URL = "https://www.bangla-kobita.com"
# output file (appended)
OUTPUT_FILE = os.path.join(os.getcwd(), "database","passage.txt")

# list of specific poet profile URLs
POET_URLS = [
    "https://www.bangla-kobita.com/rabindranath/",
    "https://www.bangla-kobita.com/sukumar/",
    "https://www.bangla-kobita.com/satyendranath/",
    "https://www.bangla-kobita.com/jibanananda/",
    "https://www.bangla-kobita.com/sukanta/",
]

# CSS selectors for poem table and links
POEMS_TABLE_SELECTOR = '#poem > div.list-js > table > tbody > tr'
POEM_LINK_SELECTOR  = 'td:nth-of-type(3) > a'

# ── Selenium setup (headless) ─────────────────────────────────────────────────
chrome_opts = Options()
chrome_opts.add_argument("--headless")
chrome_opts.add_argument("--disable-gpu")
chrome_opts.add_argument("--no-sandbox")
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_opts
)

# ── Helpers ───────────────────────────────────────────────────────────────────
def make_soup(url, wait=2):
    driver.get(url)
    time.sleep(wait)
    return BeautifulSoup(driver.page_source, "html.parser")

def get_poem_text(soup):
    # find poem title as <h1> then collect siblings until <h2>
    title_tag = soup.find("h1")
    if not title_tag:
        return None
    lines = []
    for sib in title_tag.next_siblings:
        if getattr(sib, 'name', None) == 'h2':
            break
        if isinstance(sib, NavigableString):
            txt = sib.strip()
            if txt:
                lines.append(txt)
        elif sib.name == 'br':
            lines.append("\n")
        else:
            txt = sib.get_text(separator="\n").strip()
            if txt:
                lines.append(txt)
    return "\n".join(lines).strip()

# ── Scrape and append ─────────────────────────────────────────────────────────
with open(OUTPUT_FILE, "a", encoding="utf-8") as fout:
    for poet_url in POET_URLS:
        # derive poet name from URL
        poet_name = poet_url.rstrip('/').split('/')[-1]
        print(f"Scraping poet: {poet_name}")
        poet_soup = make_soup(poet_url)
        rows = poet_soup.select(POEMS_TABLE_SELECTOR)
        if not rows:
            print(f"  No poems found for {poet_name}")
            continue

        for row in rows:
            link = row.select_one(POEM_LINK_SELECTOR)
            if not link:
                continue
            title = link.get_text(strip=True)
            href = link['href']
            poem_url = href if href.startswith('http') else BASE_URL + href
            print(f"  → {title}")
            poem_soup = make_soup(poem_url)
            text = get_poem_text(poem_soup)
            if not text:
                print(f"    (no content for {title})")
                continue
            fout.write(f"=== {poet_name} — {title} ===\n")
            fout.write(text + "\n\n")
            time.sleep(1)

# ── Cleanup ─────────────────────────────────────────────────────────────────────
driver.quit()
print(f"Done. Appended poems to {OUTPUT_FILE}")
