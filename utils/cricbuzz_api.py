import re
import requests
from bs4 import BeautifulSoup


CRICBUZZ_BASE_URL = "https://www.cricbuzz.com"


def get_match_commentary(match_id):
    url = f"{CRICBUZZ_BASE_URL}/api/mcenter/comm/{match_id}"

    response = requests.get(
        url,
        timeout=15,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json,text/plain,*/*",
            "Referer": "https://www.cricbuzz.com/"
        }
    )

    response.raise_for_status()
    return response.json()


def get_cricbuzz_matches():
    url = f"{CRICBUZZ_BASE_URL}/live-cricket-scores"

    response = requests.get(
        url,
        timeout=15,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    matches = []
    seen_ids = set()

    for link in soup.find_all("a", href=True):
        href = link.get("href", "")

        match = re.search(
            r"/live-cricket-scores/(\d+)/([^/]+)",
            href
        )

        if not match:
            continue

        match_id = match.group(1)
        slug = match.group(2)

        if match_id in seen_ids:
            continue

        seen_ids.add(match_id)

        title = link.get_text(" ", strip=True)

        if not title:
            title = slug.replace("-", " ").title()

        matches.append(
            {
                "match_id": match_id,
                "title": title,
                "url": f"{CRICBUZZ_BASE_URL}{href}"
            }
        )

    return matches