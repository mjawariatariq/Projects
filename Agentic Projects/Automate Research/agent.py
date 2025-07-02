from web_scraper import scrape_websites
from utils import summarize, generate_report
SITES = [
    "https://arxiv.org",
    "https://arxiv.org/list/cs.AI/recent",
    "https://paperswithcode.com",
    "https://allenai.org",
    "https://openai.com/blog",
    "https://ai.googleblog.com",
    "https://www.deepmind.com/blog",
    "https://aiindex.stanford.edu"
]
# test one known accessible site

# def run_agentic_research(query):
#     scraped_data = scrape_websites(query, SITES)

#     if not scraped_data:
#         return "## No relevant information found\n\nTry a different search query or check back later."

#     summary = summarize(scraped_data, query)
#     report = generate_report(summary)
#     return report


def run_agentic_research(query):
    scraped_data = scrape_websites(query, SITES)

    if not scraped_data:
        return {
            "summary": "No relevant information found.",
            "sources": []
        }

    summary = summarize(scraped_data, query)
    report = generate_report(summary)
    sources = [item["site"] for item in scraped_data]

    return {
        "summary": report,
        "sources": sources
    }
