from urllib import request
from flask import Flask,redirect,url_for,request,render_template
from pymongo import MongoClient
from bs4 import BeautifulSoup
import os
import requests
app=Flask(__name__)

client=MongoClient(os.environ["DB_PORT_27017_TCP_ADDR"],27017)
db=client.scrapedb

@app.route('/')
def scraper():

    _items=db.scrapedb.find()
    items=[item for item in _items]
    return render_template('todo.html',items=items)

@app.route("/new",methods=["POST"])
def new():

    # Get the link in text. Here request is a flask object. whereas requests is a module for accessing urls
    headers = {'User-Agent': 'Mozilla/5.0'}
    link=request.form['url']
    source=requests.get(link,headers=headers).text
    soup=BeautifulSoup(source,"html.parser")

    itemnames=[]
    prices=[]
    tags=soup.find_all("div", class_="s-item__info clearfix")
    for i in tags:
        itemname = i.find("h3", class_= "s-item__title")
        price = i.find("span", class_= "s-item__price")
        itemnames.append(itemname.text)
        prices.append(price.text)
      
        
    list=[
        
    ]
    item_doc={
        'name':itemnames,
        'price':prices
    }

    
    db.scrapedb.insert_one(item_doc)
    
    
    return redirect(url_for('scraper'))



if __name__=="__main__":
    app.run(host='0.0.0.0',debug=True)


