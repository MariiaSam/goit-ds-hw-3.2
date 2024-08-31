import requests
from bs4 import BeautifulSoup
import json

def get_author_details(author_url):

    response = requests.get(author_url)
    soup = BeautifulSoup(response.text, 'lxml')
    
    fullname = soup.find('h3', class_='author-title').text.strip()
    born_date = soup.find('span', class_='author-born-date').text.strip()
    born_location = soup.find('span', class_='author-born-location').text.strip()
    description = soup.find('div', class_='author-description').text.strip()
    
    return {
        "fullname": fullname,
        "born_date": born_date,
        "born_location": born_location,
        "description": description
    }

def get_authors():
    url = 'https://quotes.toscrape.com/'
    authors_data = []
    authors_seen = set() 
    
    while url:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        authors = soup.find_all('small', class_='author')
        
        for author in authors:
            author_name = author.text.strip()
            
            if author_name not in authors_seen:
                authors_seen.add(author_name)
                author_url = 'https://quotes.toscrape.com' + author.find_next_sibling('a')['href']
                author_details = get_author_details(author_url)
                authors_data.append(author_details)
        
        next_btn = soup.find('li', class_='next')
        if next_btn:
            next_url = next_btn.find('a')['href']
            url = 'https://quotes.toscrape.com' + next_url
        else:
            url = None
    
    with open('authors.json', 'w') as f:
        json.dump(authors_data, f, ensure_ascii=False, indent=4)

    return 'authors.json'

get_authors()
