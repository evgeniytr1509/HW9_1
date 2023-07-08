import requests
from bs4 import BeautifulSoup
import json

# Функция для извлечения информации о цитатах
def scrape_quotes():
    quotes = []
    page = 1
    while True:
        url = f"http://quotes.toscrape.com/page/{page}/"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        quote_divs = soup.find_all('div', class_='quote')
        if not quote_divs:
            break
        for quote_div in quote_divs:
            quote = {
                'quote': quote_div.find('span', class_='text').get_text(),
                'author': quote_div.find('small', class_='author').get_text(),
                'tags': [tag.get_text() for tag in quote_div.find_all('a', class_='tag')]
            }
            quotes.append(quote)
        page += 1
    return quotes

# Функция для извлечения ссылок на авторов
def scrape_author_urls(quotes):
    author_urls = []
    for quote in quotes:
        author_url = f"http://quotes.toscrape.com/author/{quote['author'].replace(' ', '-')}/"
        if author_url not in author_urls:
            author_urls.append(author_url)
    return author_urls

# Функция для извлечения информации об авторе
def scrape_author_details(author_url):
    response = requests.get(author_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    born_date = soup.find('span', class_='author-born-date').get_text()
    born_location = soup.find('span', class_='author-born-location').get_text()[3:]
    description = soup.find('div', class_='author-description').get_text().strip()
    author = {
        'fullname': soup.find('h3', class_='author-title').get_text().strip(),
        'born_date': born_date,
        'born_location': born_location,
        'description': description
    }
    return author

# Скрапинг цитат
quotes = scrape_quotes()

# Запись цитат в файл quotes.json
with open('quotes.json', 'w') as f:
    json.dump(quotes, f, indent=4)

# Скрапинг информации об авторах и их деталей
author_urls = scrape_author_urls(quotes)
authors_with_details = [scrape_author_details(author_url) for author_url in author_urls]

# Запись информации об авторах в файл authors.json
with open('authors.json', 'w') as f:
    json.dump(authors_with_details, f, indent=4)
