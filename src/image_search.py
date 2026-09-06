import requests
import sys
import os
from urllib.parse import quote
from bs4 import BeautifulSoup

# Add parent directory to access config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

def search_image(image_url: str):
    """
    Performs a reverse image search using Google Images (via scrape.do as the fetch proxy).
    `image_url` must be a PUBLICLY accessible URL to the face image
    (e.g. a raw GitHub link to sample_data/sample_face.jpg).

    Returns matched post details: {post_url, title, snippet, source, timestamp}.
    """
    if not config.SCRAPE_DO_API_KEY or config.SCRAPE_DO_API_KEY == "your_scrape_do_key_here":
        raise ValueError("SCRAPE_DO_API_KEY is not set or is invalid in .env file.")

    # Build the Google reverse image search URL
    google_search_url = f"https://www.google.com/searchbyimage?image_url={quote(image_url, safe='')}&safe=off"

    # Route the request through scrape.do, with JS rendering enabled
    scrape_do_endpoint = "https://api.scrape.do/"
    params = {
        "token": config.SCRAPE_DO_API_KEY,
        "url": google_search_url,
        "render": "true"
    }

    try:
        response = requests.get(scrape_do_endpoint, params=params, timeout=60)
        response.raise_for_status()
        html = response.text

        soup = BeautifulSoup(html, "html.parser")

        # Google's reverse image results list pages under result blocks with <a> tags
        # linking to the matching page, and a heading/snippet nearby.
        results = []
        for result_block in soup.select("div.g"):
            link_tag = result_block.select_one("a")
            title_tag = result_block.select_one("h3")
            snippet_tag = result_block.select_one("div.VwiC3b, span.aCOpRe")

            if link_tag and title_tag:
                results.append({
                    "post_url": link_tag.get("href", ""),
                    "title": title_tag.get_text(strip=True),
                    "snippet": snippet_tag.get_text(strip=True) if snippet_tag else "",
                    "source": link_tag.get("href", "").split("/")[2] if link_tag.get("href") else "",
                    "timestamp": "Unknown"
                })

        if results:
            return results[0]  # top match

        return None  # No results found

    except Exception as e:
        raise RuntimeError(f"Error during image search: {e}")