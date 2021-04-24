import requests
from bs4 import BeautifulSoup
import csv

base_url = 'http://books.toscrape.com/'
catalogue_selected_product_url = 'catalogue/a-light-in-the-attic_1000'

response = requests.get(base_url + catalogue_selected_product_url)

soup = BeautifulSoup(response.content, 'html.parser')
product_page_url = base_url + catalogue_selected_product_url


def get_universal_product_code():
  universal_product_code = soup.select_one('table > tr > td').text
  return universal_product_code


def get_title():
  title = soup.select_one('h1').text
  return title


def get_price_including_tax():
  price_including_tax = soup.select('table > tr')[3].select_one('td').text
  return price_including_tax


def get_price_excluding_tax():
  price_excluding_tax = soup.select('table > tr')[2].select_one('td').text
  return price_excluding_tax


def get_number_available():
  number_available = soup.select('table > tr')[5].select_one('td').text
  return number_available


def get_product_description():
  product_description = soup.select_one('.sub-header + p').text
  return product_description


def get_category():
  category = soup.select('.breadcrumb > li')[2].select_one('a').text
  return category


def get_review_rating():
  review_rating = soup.select('table > tr')[6].select_one('td').text
  return review_rating


def get_image_url():
  image = soup.select_one('.item > img')
  image_url = base_url + image['src'].replace('../', '')
  return image_url
  


def save_book_informations_to_csv(book_informations: dict):
  with open(f'books.csv', 'w', encoding='utf-8-sig') as csv_file:
    writer = csv.DictWriter(csv_file, book_informations, dialect='excel')
    writer.writeheader()
    writer.writerow(book_informations)


def get_book_informations(url):
  if response.status_code == 200:
    book_informations = {
      'universal_product_code': get_universal_product_code(),
      'title': get_title(),
      'price_including_tax': get_price_including_tax(),
      'get_price_excluding_tax': get_price_excluding_tax(),
      'number_available': get_number_available(),
      'product_description': get_product_description(),
      'category': get_category(),
      'review_rating': get_review_rating(),
      'image_url': get_image_url()
    }
    save_book_informations_to_csv(book_informations)


get_book_informations(product_page_url)
