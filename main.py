from http.client import PROXY_AUTHENTICATION_REQUIRED
from bs4 import BeautifulSoup
from requests import get
from sys import argv
from datetime import datetime
import sqlite3
date=datetime.today().strftime('%Y-%m-%d')

connection=sqlite3.connect('data.db')
cursor=connection.cursor()

#sqlite3 table setup
if(len(argv)==2 and argv[1]=='-setup'):
    cursor.execute('CREATE TABLE items (link TEXT, price REAL,date TEXT)')

def get_price(bs)->float:
    text = bs.find('div', class_="main-price is-big")
    text = text.get_text()[:-3]
    text=text.replace(" ",".")
    price=float(text)
    return price

f=open('links.txt','r')
link_array=f.readlines()

for link in link_array:
    link=link.replace('\n','')
    
    page=get(link)
    bs = BeautifulSoup(page.content, 'html.parser')
    price = get_price(bs)
    cursor.execute('INSERT INTO items VALUES (?,?,?)',(link,price,date))
    connection.commit()
    print(price,link)
    

connection.close()