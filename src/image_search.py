import sys
import os
import requests

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

def search_image(image_url: str):
    """
    Performs a reverse image search using SerpApi's Google Reverse Image engine.
    `image_url` must be a PUBLICLY accessible URL to the face image.

    Returns a list of candidate matched post details:
    {post_url, title, snippet, source, timestamp, image_url}.
    """
    if not config.SERPAPI_KEY:
        print("Search service unavailable. Please check API configuration/network connectivity.")
        return []

    endpoint = "https://serpapi.com/search.json"
    params = {
        "engine": "google_reverse_image",
        "image_url": image_url,
        "api_key": config.SERPAPI_KEY
    }

    try:
        response = requests.get(endpoint, params=params, timeout=60)
        response.raise_for_status()
        data = response.json()

        results = []
        image_results = data.get("image_results", [])

        # TEMPORARY DEBUG
        print(f"      [debug] {len(image_results)} raw image_results returned")
        print(f"      [debug] first 3 titles: {[m.get('title','') for m in image_results[:3]]}")
        print(f"      [debug] first 3 links: {[m.get('link','') for m in image_results[:3]]}")

        for match in image_results:
            results.append({
                "post_url": match.get("link", ""),
                "title": match.get("title", ""),
                "snippet": match.get("snippet", ""),
                "source": match.get("source", ""),
                "timestamp": "Unknown",
                "image_url": match.get("thumbnail", "")
            })

        print(f"      [debug] {len(results)} candidates parsed, "
              f"{sum(1 for r in results if r['image_url'])} have image URLs")

        return results

    except Exception as e:
        print(f"Search service unavailable. Please check API configuration/network connectivity. ({e})")
        return []