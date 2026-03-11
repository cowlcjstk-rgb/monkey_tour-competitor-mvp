import requests
from bs4 import BeautifulSoup

def scrape_product_page(url: str) -> str:
    try:
        response = requests.get(url, timeout=20, headers={
            "User-Agent": "Mozilla/5.0"
        })
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        text = soup.get_text(separator="\n")
        cleaned = "\n".join(line.strip() for line in text.splitlines() if line.strip())
        return cleaned[:15000]

    except Exception as e:
        return f"SCRAPE_ERROR: {str(e)}"
