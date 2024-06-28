# Scripts para web scraping usando BeautifulSoup, Scrapy, Selenium

from bs4 import BeautifulSoup
import requests

def extract_educational_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    content = []
    for item in soup.find_all('div', class_='educational-content'):
        content.append(item.text)
    return content
