import requests
from bs4 import BeautifulSoup
import re
from fake_useragent import UserAgent

TIMEOUT = 10
from fake_useragent import UserAgent

try:
    ua = UserAgent()
    user_agent = ua.random
except:
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115 Safari/537.36"



def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\n+', '\n', text)
    return text.strip()

def scrape_websites(query, sites):
    results = []
    ua = UserAgent()
    
    for site in sites:
        try:
            headers = {
    'User-Agent': user_agent,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://www.google.com/'
}

            
            response = requests.get(site, headers=headers, timeout=TIMEOUT)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Remove unwanted elements
            for element in soup(["script", "style", "nav", "footer", "iframe", "noscript"]):
                element.decompose()
                
            text = soup.get_text(separator=' ', strip=True)
            text = clean_text(text)
            
            if query.lower() in text.lower():
                results.append({
                    "site": site,
                    "text": text[:5000]  # Limit text length
                })
                
        except Exception as e:
            print(f"Error scraping {site}: {str(e)[:100]}")  # Truncate long error messages
            continue
            
    return results
