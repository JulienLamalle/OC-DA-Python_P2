import requests
from bs4 import BeautifulSoup
class Scheduler:

  def get_user_name(self, base_url, scheduler, c, b):
    print('Bonjour, quel est votre prénom ?')
    user_name = str(input())
    self.offer_the_features(user_name, base_url, scheduler, c, b)

  def offer_the_features(self, user_name, base_url, scheduler, c, b):
    print(f'Je peux te proposer plusieurs choses que voici {user_name}:')
    print('1. Scrapper tout le site')
    print('2. Scrapper seulement une catégorie')
    print('3. Scrapper seulement un livre')
    user_choice = 0
    while user_choice not in range(1, 4):
      try:
        user_choice = int(input('Choisissez une option du menu: '))
      except (ValueError, TypeError):
        pass
    self.perform(user_choice, base_url, scheduler, c, b)

  def display_category_to_user(self, categories, b, base_url, c, user_choice):
    print('Chosissez la catégorie qui vous intéresse et saisissez le numéro correspondant à celle-ci')
    for num, category in enumerate(categories, start=1):
      print(f'{num}. {category}')
    user_category_choice = 0
    while user_category_choice not in range(1, 51):
      try:
        user_category_choice = int(input('Choisissez une option du menu: '))
      except (ValueError, TypeError):
        pass
    values = list(categories.values())
    url = values[user_category_choice - 1]
    categories = list(categories)
    category = categories[user_category_choice - 1]
    c.get_all_books_link(url, category, base_url, b, user_choice)
  
  def url_exists_get(self, url: str, b, base_url):
    try:
      response = requests.get(url)
      soup = BeautifulSoup(response.content, 'html.parser')
      try:
        response.raise_for_status()
        category = b.get_category(soup)
        b.get_book_informations(url, category, base_url)
      except requests.exceptions.HTTPError:
        return False
    except requests.exceptions.ConnectionError:
      return False

  def get_user_book_choice(self, b, base_url):
    print("Pour que je puisse scrapper un livre pour vous merci de vous rendre sur l'url suivante et de me donner le lien du livre souhaité => http://books.toscrape.com/")
    user_book_choice = str(input('Merci de me fournir une url valide: '))
    while 'http' not in user_book_choice:
      user_book_choice = str(input('Merci de me fournir une url valide: '))
    else:
      self.url_exists_get(user_book_choice, b, base_url)


  def perform(self, user_choice, base_url, scheduler, c, b):
    if user_choice == 1 or user_choice == 2:
      c.get_all_categories_links(base_url, b, user_choice, scheduler, c)
    elif user_choice == 3:
      self.get_user_book_choice(b, base_url)
