import requests

def fetch_papers_from_core(query):
    """
    Fetches papers from the CORE API based on the query.
    """
    search_url = "https://api.core.ac.uk/v3/search/works/"
    params = {
        "q": query,
        "limit": 10  # Limiting to 10 results for now
    }
    response = requests.get(search_url, params=params)
    response.raise_for_status()  # Raise an exception for bad status codes

    data = response.json()

    papers = []
    for item in data.get("results", []):
        papers.append({
            "title": item.get("title"),
            "authors": [author.get("name") for author in item.get("authors", [])],
            "year": item.get("yearPublished"),
            "content": item.get("abstract", ""),
            "pdf_url": item.get("downloadUrl")
        })

    return papers
