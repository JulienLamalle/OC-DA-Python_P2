import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from math import ceil
class Category:
  
  def get_all_categories_links(self, url, b, user_choice, scheduler, c):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    if response.status_code == 200:
      categories_informations = soup.select('.nav-list > li > ul > li > a')
      categories = {}
      for category_informations in categories_informations:
        category_url = category_informations['href'].replace('index.html', '')
        categories.update({category_informations.text.replace('\n','').replace(' ', '') : url + '/' + category_url })
      if user_choice == 1:
        for category in categories:
          self.get_all_books_link(categories[category], category, url, b, user_choice)
      elif user_choice == 2:
        scheduler.display_category_to_user(categories, b, url, c, user_choice)
      
  def get_all_books_link(self, url, category, base_url, b, user_choice):
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
      if user_choice == 1 or user_choice == 2:
        with tqdm(total=100) as pbar:
          for book_url in final_books_urls:
            b.get_book_informations(book_url, category, base_url)
            pbar.update(ceil((1/len(final_books_urls))*100))
          self.get_next_page(soup, url, category, base_url, b, user_choice)
      else:
        return
  
  def get_next_page(self, soup, url, category, base_url, b, user_choice):
    next_button = soup.select_one('.next > a')
    if next_button:
      next_page_link = url + next_button['href']
      self.get_all_books_link(next_page_link, category, base_url, b, user_choice)
    else:
      return