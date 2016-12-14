from BeautifulSoup import BeautifulSoup as BS
#import pandas as pd
from StringIO import StringIO
from collections import namedtuple
import os
from pprint import pprint
from HTMLParser import HTMLParser


def next_feed(soup):
    feedlist = soup.find("ul", {"class":"pagination"})
    nexturl=None
    if feedlist:
        base,curix=feedlist.find("li",{"class":"active"}).a.get("href").split("=")
        _,lastix=feedlist.find_all("li")[-1].a.get("href").split("=")
        if int(curix) < int(lastix):
            nexturl = base+"="+str(int(curix)+1)
        
    return nexturl




def parser_product(html):
    #soup=BS(html)
    soup=BeautifulSoup(html,"html5lib")
    feedbacks=[]
    ptype="/".join(soup.find("ol", {"class":"breadcrumb"}).text.strip().split("\n")[1].split("      ")[1:])
    li = soup.find_all("div",{"class":"row"})[1].find("div",{'class':"col-md-8"})
    Entry=namedtuple('Entry', ['product_id','product', 'price_usd', "price_btc",
                     "vendor","vendor_url","product_type",
                    'delivery'])

    #li = soup.findAll("div",{"class":"row"})[1].find("div",{'class':"col-md-8"})


    entry = { 'product_id':li.form.get('action'),
    'product':li.h2.text,
    'price_usd':li.find("div",{"class":"listing-price"}).strong.text.strip(),
    'price_btc':li.find("div",{"class":"listing-price"}).span.text.strip(),
    'vendor':li.tr.findAll("td")[1].a.text,
    'vendor_url':li.tr.findAll("td")[1].a["href"], 
    'product_type':ptype,        
    'delivery':li.findAll("td")[5].text,        
    #'description':soup.p.text
    }

    return Entry(**entry)

def parser_feedback(html):
    soup=BeautifulSoup(html,"html5lib")
    feedbacks=[]
    li = soup.find_all("div",{"class":"row"})[1].find("div",{'class':"col-md-8"})
    prod=li.form.get('action')
    Feedback = namedtuple("Feedback", ["prod_id","date",'user',"delivery_time", "note", "text"])
    h=HTMLParser()
    try:
        for e in soup.find_all("table",{"class":"table"})[2].tbody.findAll("tr"):
            feed,text,deliv,user,date=e.find_all('td')
            feed=feed.span.get("class")[1].split("-")[1] 
            note=0
            if feed == 'danger':
                note=-1
            if feed == "default":
                note=0
            if feed == "success":
                note=1
        #print "||".join([date.text,user.text, h.unescape(text.text),  deliv.text])
            f=Feedback(prod,date.text,user.text,deliv.text, note, text.text)
            feedbacks.append(f)
    except AttributeError, e:
        print e
        
    
    other_feedback = next_feed(soup)
    
        
    return other_feedback,feedbacks
        

