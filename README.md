# Project 2 (Julien Lamalle)

### This project was done in python <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="30" height="30"/>

You can use this repo to scrape data from this [website](http://books.toscrape.com/).

```
product_page_url

universal_ product_code (upc)

title

price_including_tax

price_excluding_tax

number_available

product_description

category

review_rating

image_url 
```

All of the above information is saved in a data folder which itself has a folder for each category, a csv file is created for each category and a folder containing the image associated with each scrapbook.

This project allows you to scrape all the books on the site, a category only, or a particular book by providing a valid url.

This project uses python and it is necessary to have it installed on your machine, if it is not the case you can download it on this [link](https://www.python.org/downloads/)

To clone this folder, execute the following command: 

```
git clone git@github.com:JulienLamalle/OC-DA-Python_P2.git
```

From your terminal you can enter the file as follows: 

```
cd OC-DA-Python_P2/
```

To avoid conflicts with potential existing projects I strongly recommend that you create a virtual environment for this project using this command:

```
python -m venv env
```

Then you have to activate your environment:

```
source env/bin/activate
```

You now need to install all the libraries necessary for this program to work properly, for this you can run the following command: 

```
pip install -r requirements.txt
```

You are now with your console in the program folder so you can launch it like this: 

```
python main.py
```

As expected, you will be able to follow the instructions that will appear in the console and then you will see the data folder containing the desired category or categories

### ENJOY 🎉 ! 