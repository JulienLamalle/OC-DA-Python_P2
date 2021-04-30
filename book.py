import requests
from bs4 import BeautifulSoup
import csv
import os
from pathlib import Path
import shutil
from slugify import slugify


class Book:
    def get_universal_product_code(self, soup):
        try:
            universal_product_code = soup.select_one("table > tr > td").text
            return universal_product_code
        except:
            return

    def get_title(self, soup):
        try:
            title = soup.select_one("h1").text
            return title
        except:
            return

    def get_price_including_tax(self, soup):
        try:
            price_including_tax = soup.select("table > tr")[3].select_one("td").text
            return price_including_tax
        except:
            return

    def get_price_excluding_tax(self, soup):
        try:
            price_excluding_tax = soup.select("table > tr")[2].select_one("td").text
            return price_excluding_tax
        except:
            return

    def get_number_available(self, soup):
        number_available = soup.select("table > tr")[5].select_one("td").text
        number_available = number_available.replace('In stock (', '').replace(' available)','')
        return number_available

    def get_product_description(self, soup):
        try:
            product_description = soup.select_one(".sub-header + p").text
            return product_description
        except:
            return

    def get_category(self, soup):
        try:
            category = soup.select(".breadcrumb > li")[2].select_one("a").text
            return category
        except:
            return

    def get_review_rating(self, soup):
        try:
            review_rating = soup.select("table > tr")[6].select_one("td").text
            return review_rating
        except:
            return

    def get_image_url(self, soup, base_url):
        try:
            image = soup.select_one(".item > img")
            image_url = base_url + "/" + image["src"].replace("../", "")
            return image_url
        except:
            return

    def get_book_informations(self, url, category, base_url):
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            if response.status_code == 200:
                book_informations = {
                    "product_page_url": url,
                    "universal_product_code": self.get_universal_product_code(soup),
                    "title": self.get_title(soup),
                    "price_including_tax": self.get_price_including_tax(soup),
                    "get_price_excluding_tax": self.get_price_excluding_tax(soup),
                    "number_available": self.get_number_available(soup),
                    "product_description": self.get_product_description(soup),
                    "category": self.get_category(soup),
                    "review_rating": self.get_review_rating(soup),
                    "image_url": self.get_image_url(soup, base_url),
                    "image_filename": slugify(self.get_title(soup)),
                }
                self.save_book_informations_to_csv(book_informations, category)
                self.save_book_image(soup, book_informations, category)
            elif not response.status_code // 100 == 2:
                print(f"Error: Unexpected response {response}")
        except requests.exceptions.RequestException as error:
            print(f"Error: {error}")

    def save_book_image(self, soup, book_informations, category):
        try:
            response = requests.get(book_informations["image_url"], stream=True)
            if response.status_code == 200:
                dir_path = f"data/{category}/images"
                filename = book_informations["image_filename"]
                if not os.path.exists(dir_path):
                    os.makedirs(f"data/{category}/images")
                file_path = os.path.join(dir_path, filename)
                response.raw.decode_content = True
                with open(f"{file_path}", "wb") as file:
                    shutil.copyfileobj(response.raw, file)
            elif not response.status_code // 100 == 2:
                print(f"Error: Unexpected response {response}")
        except requests.exceptions.RequestException as error:
            print(f"Error: {error}")

    def save_book_informations_to_csv(self, book_informations: dict, category):
        dir_path = f"data/{category}"
        filename = f"{category}.csv"
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path, exist_ok=True)
        file_path = os.path.join(dir_path, filename)
        with open(f"{file_path}", "a", encoding="utf-8-sig") as csv_file:
            writer = csv.DictWriter(csv_file, book_informations, dialect="excel")
            if Path(f"{file_path}").stat().st_size == 0:
                writer.writeheader()
            writer.writerow(book_informations)
