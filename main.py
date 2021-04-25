from category import Category
from book import Book

base_url = 'http://books.toscrape.com'

b = Book()
category = Category()

category.get_all_categories_links(base_url, b)


