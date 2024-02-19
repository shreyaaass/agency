import requests
from bs4 import BeautifulSoup

def scrape_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    for br in soup.find_all('br'):
        br.replace_with('')
    
    content = soup.select_one('.big-article')
    return content.text.strip() if content else None

with open('mar.txt', 'r') as file:
    urls = file.read().splitlines()
with open('contents.txt', 'w', encoding='utf-8') as output_file:
    for url in urls:
        content = scrape_content(url)
        if content:
            output_file.write(content.replace("\n","")+"\n\n")
        else:
            print(f"Could not scrape content from {url}")

print("Scraping complete. Check contents.txt for the results.")