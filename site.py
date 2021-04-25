import requests
from bs4 import BeautifulSoup
import csv
import os
from pathlib import Path
import shutil 
from slugify import slugify

base_url = 'http://books.toscrape.com'

def get_all_categories_links(url):
  response = requests.get(url)
  soup = BeautifulSoup(response.content, 'html.parser')
  if response.status_code == 200:
    categories_informations = soup.select('.nav-list > li > ul > li > a')
    categories = {}
    for category_informations in categories_informations:
      category_url = category_informations['href'].replace('index.html', '')
      categories.update({category_informations.text.replace('\n','').replace(' ', '') : base_url + '/' + category_url })
    for category in categories:
      get_all_books_link(categories[category], category)

def get_all_books_link(url, category):
  response = requests.get(url)
  soup = BeautifulSoup(response.content, 'html.parser')
  if response.status_code == 200:
    dirty_books_urls = soup.select('h3 > a')
    final_books_urls = []
    for book_url in dirty_books_urls:
      book_url = book_url['href'].replace('../', '').split('/')
      del book_url[-1]
      for book in book_url:
        final_books_urls.append(base_url + '/catalogue/' + book)
    for book_url in final_books_urls:
      get_book_informations(book_url, category)
    get_next_page(soup, url, category)


def get_universal_product_code(soup):
  try:
    universal_product_code = soup.select_one('table > tr > td').text
    return universal_product_code
  except: 
    return


def get_title(soup):
  try:
    title = soup.select_one('h1').text
    return title
  except: 
    return

def get_price_including_tax(soup):
  try:
    price_including_tax = soup.select('table > tr')[3].select_one('td').text
    return price_including_tax
  except: 
    return

def get_price_excluding_tax(soup):
  try:
    price_excluding_tax = soup.select('table > tr')[2].select_one('td').text
    return price_excluding_tax
  except: 
    return

def get_number_available(soup):
  number_available = soup.select('table > tr')[5].select_one('td').text
  return number_available


def get_product_description(soup):
  try: 
    product_description = soup.select_one('.sub-header + p').text
    return product_description
  except: 
    return

def get_category(soup):
  try: 
    category = soup.select('.breadcrumb > li')[2].select_one('a').text
    return category
  except: 
    return


def get_review_rating(soup):
  try:
    review_rating = soup.select('table > tr')[6].select_one('td').text
    return review_rating
  except: 
    return

def get_image_url(soup):
  try: 
    image = soup.select_one('.item > img')
    image_url = base_url + '/' + image['src'].replace('../', '')
    return image_url
  except: 
    return


def get_next_page(soup, url, category):
  next_button = soup.select_one('.next > a')
  if next_button:
    next_page_link = url + next_button['href']
    get_all_books_link(next_page_link, category)
  else: 
    return

def get_book_informations(url, category):
  response = requests.get(url)
  soup = BeautifulSoup(response.content, 'html.parser')
  if response.status_code == 200:
    book_informations = {
      'universal_product_code': get_universal_product_code(soup),
      'title': get_title(soup),
      'price_including_tax': get_price_including_tax(soup),
      'get_price_excluding_tax': get_price_excluding_tax(soup),
      'number_available': get_number_available(soup),
      'product_description': get_product_description(soup),
      'category': get_category(soup),
      'review_rating': get_review_rating(soup),
      'image_url': get_image_url(soup),
      'image_filename': slugify(get_title(soup))
    }
    save_book_informations_to_csv(book_informations, category)
    save_book_image(soup, book_informations, category)
    
def save_book_image(soup, book_informations, category):
  response = requests.get(book_informations['image_url'], stream = True)
  if response.status_code == 200:
    dir_path = f'data/{category}/images'
    filename = book_informations['image_filename']
    if not os.path.exists(dir_path):
      os.makedirs(f'data/{category}/images')
    file_path = os.path.join(dir_path, filename)
    response.raw.decode_content = True
    with open(f'{file_path}', 'wb') as file:
      shutil.copyfileobj(response.raw, file)

def save_book_informations_to_csv(book_informations: dict, category):
  dir_path = f'data/{category}'
  filename = f'{category}.csv'
  if not os.path.isdir(dir_path):
    os.makedirs(dir_path, exist_ok=True)
  file_path = os.path.join(dir_path, filename)
  with open(f'{file_path}', 'a', encoding='utf-8-sig') as csv_file:
    writer = csv.DictWriter(csv_file, book_informations, dialect='excel')
    if Path(f"{file_path}").stat().st_size == 0:
      writer.writeheader()
    writer.writerow(book_informations)

def perform(url):
  get_all_categories_links(url)


perform(base_url)
