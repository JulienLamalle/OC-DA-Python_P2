from scheduler import Scheduler
from category import Category
from book import Book
from colorama import init
class Main:
  
  def __init__(self, base_url):
    self.base_url = base_url
  

  def perform(self, base_url):
    b = Book()
    c = Category()
    scheduler = Scheduler()
    scheduler.get_user_name(base_url, scheduler, c , b)

if __name__ == '__main__':
  base_url = 'http://books.toscrape.com'
  init(autoreset=True)
  main = Main(base_url)
  main.perform(base_url)