import requests
from bs4 import BeautifulSoup
import json

def get_quotes():
    url = 'https://quotes.toscrape.com/'
    quotes_data = []
    
    while url:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        quotes = soup.find_all('div', class_='quote')

        for quote in quotes:
            tags = [tag.text.strip() for tag in quote.find_all('a', class_='tag')]
            author = quote.find('small', class_='author').text.strip()
            text = quote.find('span', class_='text').text.strip()
            
            quotes_data.append({
                "tags": tags,
                "author": author,
                "quote": text,
            })
        
        next_btn = soup.find('li', class_='next')
        if next_btn:
            next_url = next_btn.find('a')['href']
            url = 'https://quotes.toscrape.com' + next_url
        else:
            url = None
    
    with open('quotes.json', 'w') as f:
        json.dump(quotes_data, f, ensure_ascii=False, indent=4)

    return 'quotes.json'

get_quotes()
