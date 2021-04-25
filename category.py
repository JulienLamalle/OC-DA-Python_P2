import requests
from bs4 import BeautifulSoup
import csv
import os
from pathlib import Path

base_url = 'http://books.toscrape.com'
category_url = '/catalogue/category/books/romance_8'


def get_all_books_link(url):
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
      get_book_informations(book_url)
    get_next_page(soup)


def get_universal_product_code(soup):
  universal_product_code = soup.select_one('table > tr > td').text
  return universal_product_code


def get_title(soup):
  title = soup.select_one('h1').text
  return title


def get_price_including_tax(soup):
  price_including_tax = soup.select('table > tr')[3].select_one('td').text
  return price_including_tax


def get_price_excluding_tax(soup):
  price_excluding_tax = soup.select('table > tr')[2].select_one('td').text
  return price_excluding_tax


def get_number_available(soup):
  number_available = soup.select('table > tr')[5].select_one('td').text
  return number_available


def get_product_description(soup):
  product_description = soup.select_one('.sub-header + p').text
  return product_description


def get_category(soup):
  category = soup.select('.breadcrumb > li')[2].select_one('a').text
  return category


def get_review_rating(soup):
  review_rating = soup.select('table > tr')[6].select_one('td').text
  return review_rating


def get_image_url(soup):
  image = soup.select_one('.item > img')
  image_url = base_url + '/' + image['src'].replace('../', '')
  return image_url


def get_next_page(soup):
  next_button = soup.select_one('.next > a')
  if next_button:
    next_page_link = base_url + category_url + '/' + next_button['href']
    print(next_page_link)
    get_all_books_link(next_page_link)
  else:
    return


def get_book_informations(url):
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
      'image_url': get_image_url(soup)
    }
    save_book_informations_to_csv(book_informations)


def save_book_informations_to_csv(book_informations: dict):
  category = 'romance'
  dir_path = f'data/{category}'
  filename = f'{category}.csv'
  if not os.path.isdir(dir_path):
    os.makedirs(dir_path, exist_ok=True)
  file_path=os.path.join(dir_path, filename)
  with open(f'{file_path}', 'a', encoding='utf-8-sig') as csv_file:
    writer = csv.DictWriter(csv_file, book_informations, dialect='excel')
    if Path(f"{file_path}").stat().st_size == 0:
      writer.writeheader()
    writer.writerow(book_informations)


def perform(url):
  get_all_books_link(url)


perform(base_url + category_url)
