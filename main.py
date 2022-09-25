from http.client import PROXY_AUTHENTICATION_REQUIRED
from bs4 import BeautifulSoup
from requests import get
from sys import argv
from datetime import datetime
import sqlite3
date=datetime.today().strftime('%Y-%m-%d')

connection=sqlite3.connect('data.db')
cursor=connection.cursor()

# sqlite3 table setup
if(len(argv)==2 and argv[1]=='-setup'):
    cursor.execute('CREATE TABLE items (link TEXT, price REAL,date TEXT)')
    exit()

if (len(argv) == 2 and argv[1] == '-delete'):
    cursor.execute('DROP TABLE items ')
    exit()
if (len(argv) == 2 and argv[1] == '-clearstart'):
    cursor.execute('DELETE FROM items ')
    


def find_text(bs):
    if bs.find('div', class_="main-price is-big")!=None:
        return bs.find('div', class_="main-price is-big")
    if bs.find('div', class_="main-price price-regular is-medium") != None:
        return bs.find('div', class_="main-price price-regular is-medium")


def text_to_int(string)->float:
    
    text = string.get_text()[:-3]
    text=' '.join(text.split()) ###space is encoded as a no breaking space
    text=text.replace(" ","")
    text=text[:-2]+"."+text[-2:]
    price=float(text)
    return price

f=open('links.txt','r')
link_array=f.readlines()

for link in link_array:
    link=link.replace('\n','')
    
    page=get(link)
    bs = BeautifulSoup(page.content, 'html.parser')
    
    text=find_text(bs)
    if text==None:
        cursor.execute('INSERT INTO items VALUES (?,?,?)', (link, 0, date))
    price=text_to_int(text)
    cursor.execute('INSERT INTO items VALUES (?,?,?)',(link,price,date))
    connection.commit()
    print(price,link)
    

connection.close()