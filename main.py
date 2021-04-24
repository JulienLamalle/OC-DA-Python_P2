import requests
from bs4 import BeautifulSoup

base_url = 'http://books.toscrape.com/'
catalogue_selected_product_url = 'catalogue/a-light-in-the-attic_1000' 

response = requests.get(base_url + catalogue_selected_product_url)

soup = BeautifulSoup(response.content, 'html.parser')
product_page_url = base_url + catalogue_selected_product_url

def get_universal_product_code():
  universal_product_code = soup.select_one('table > tr > td')
  print("universal_product_code =>", universal_product_code.text)
  
def get_title():
  title = soup.select_one('h1')
  print('title =>', title.text)
  
def get_price_including_tax():
  price_including_tax = soup.select('table > tr')[3].select_one('td')
  print('price_including_tax =>', price_including_tax.text)
  
def get_price_excluding_tax():
  price_excluding_tax = soup.select('table > tr')[2].select_one('td')
  print('price_excluding_tax =>', price_excluding_tax.text)
  
def get_number_available():
  number_available = soup.select('table > tr')[5].select_one('td')
  print('number_available =>', number_available.text)
  
def get_product_description():
  product_description = soup.select_one('.sub-header + p')
  print('product_description =>', product_description.text)
  
def get_category():
  category = soup.select('.breadcrumb > li')[2].select_one('a')
  print('category =>', category.text)
  
def get_review_rating():
  review_rating = soup.select('table > tr')[6].select_one('td')
  print('review_rating =>', review_rating.text)
  
def get_image_url():
  image = soup.select_one('.item > img')
  image_url = base_url + image['src'].replace('../', '')
  print('image_url =>', image_url)
    
def get_book_informations(url):
  if response.status_code == 200:
    get_universal_product_code()
    get_title()
    get_price_including_tax()
    get_price_excluding_tax()
    get_number_available()
    get_product_description()
    get_category()
    get_review_rating()
    get_image_url()

get_book_informations(product_page_url)