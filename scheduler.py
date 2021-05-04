import requests
from bs4 import BeautifulSoup
from colorama import Fore


class Scheduler:
    def get_user_name(self, base_url, scheduler, catie, bookie):
        print(Fore.CYAN + "Bonjour, quel est votre prénom ?")
        user_name = str(Fore.CYAN + input())
        self.offer_the_features(user_name, base_url, scheduler, catie, bookie)

    def offer_the_features(self, user_name, base_url, scheduler, catie, bookie):
        print(
            Fore.CYAN + f"Je peux te proposer plusieurs choses que voici {user_name}:"
        )
        print(Fore.BLUE + "1. Scrapper tout le site")
        print(Fore.MAGENTA + "2. Scrapper seulement une catégorie")
        print(Fore.RED + "3. Scrapper seulement un livre")
        user_choice = 0
        while user_choice not in range(1, 4):
            try:
                user_choice = int(input("Choisissez une option du menu: "))
            except (ValueError, TypeError):
                pass
        self.perform(user_choice, base_url, scheduler, catie, bookie)

    def display_category_to_user(self, categories, bookie, base_url, catie, user_choice):
        print(
            "Chosissez la catégorie qui vous intéresse et saisissez le numéro correspondant à celle-ci"
        )
        for num, category in enumerate(categories, start=1):
            print(f"{num}. {category}")
        user_category_choice = 0
        while user_category_choice not in range(1, 51):
            try:
                user_category_choice = int(input("Choisissez une option du menu: "))
            except (ValueError, TypeError):
                pass
        values = list(categories.values())
        url = values[user_category_choice - 1]
        categories = list(categories)
        category = categories[user_category_choice - 1]
        catie.get_all_books_link(url, category, base_url, bookie, user_choice)

    def url_checker(self, url: str, bookie, base_url):
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            try:
                response.raise_for_status()
                category = bookie.get_category(soup)
                bookie.get_book_informations(url, category, base_url)
            except requests.exceptions.HTTPError:
                self.get_user_book_choice(bookie, base_url)
        except requests.exceptions.ConnectionError:
            self.get_user_book_choice(bookie, base_url)

    def get_user_book_choice(self, bookie, base_url):
        print(
            Fore.CYAN
            + "Pour que je puisse scrapper un livre pour vous merci de vous rendre sur l'url suivante et de me donner le lien du livre souhaité => http://books.toscrape.com/"
        )
        user_book_choice = str(input("Merci de me fournir une url valide: "))
        while "http" not in user_book_choice:
            user_book_choice = str(input("Merci de me fournir une url valide: "))
        else:
            self.url_checker(user_book_choice, bookie, base_url)

    def perform(self, user_choice, base_url, scheduler, catie, bookie):
        if user_choice == 1 or user_choice == 2:
            catie.get_all_categories_links(base_url, bookie, user_choice, scheduler, catie)
        elif user_choice == 3:
            self.get_user_book_choice(bookie, base_url)
