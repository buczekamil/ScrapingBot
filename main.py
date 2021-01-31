import pandas as pd
from bs4 import BeautifulSoup
import requests

html = requests.get('https://rpa.hybrydoweit.pl/').text
soup = BeautifulSoup(html, 'html.parser')

# Select articles section
articles = soup.find('section', {'id': 'articles'})

# Find necessary elements from the section
titles = articles.find_all('h3', {'class': 'rpa-article-card__title'})
links = articles.find_all('a', {'class': 'rpa-article-card__link'})
industries = articles.find_all('li', {'class': 'rpa-article-card__metadata-item'})

# Create lists of elements and append appropriate values
links_list = []
titles_list = []
industries_list = []
for link in links:
    links_list.append(link.get('href'))
for title in links:
    titles_list.append(title.get('title'))
for industry in industries:
    industry = industry.get_text()
    industry = industry.split(": ")[1:]
    i = 0
    for i in range(len(industry)):
        industries_list.append(industry[i])
        i = i + 1

# Validate and create csv file
if len(industries_list) == len(links_list) == len(titles_list):
    df = pd.DataFrame(list(zip(*[titles_list, industries_list, links_list])))
    df.columns = ['Tytuł', 'Branża/dział', 'Link do artykułu']
    df.to_csv('data.csv', index=False)
else:
    print("Pobrane dane są niekompletne")
