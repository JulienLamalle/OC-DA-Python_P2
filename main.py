from scheduler import Scheduler
from category import Category
from book import Book
from colorama import init
class Main:
  
  base_url = 'http://books.toscrape.com'

  def perform(self, base_url):
    b = Book()
    c = Category()
    scheduler = Scheduler()
    scheduler.get_user_name(base_url, scheduler, c , b)

if __name__ == '__main__':
  init(autoreset=True)
  main = Main()
  main.perform(main.base_url)