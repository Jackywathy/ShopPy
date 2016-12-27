import bs4
fakeReq = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
import requests
isNode = {'node',
             'node-teaser',
             'node-product-book',
             'node-product-book-teaser',
             'node-product',
             'node-product-teaser',
             'clear-block'
          }
isPrice = {'uc-price-product',
           'uc-price-display',
           'uc-price'
           }
K_LIST_ITEM = 'li'

class OutOfHTMLException(Exception):
    """OUCH! you've run out of html to parse...."""
    ...
def getAuthor(tag):
    if tag.get("class", None) and "field-item" in tag['class']:
        return True
    return False

def getMainProductImage(tag):
    if tag.get("class", None) and "main-product-image" in tag['class']:
        return True
    return False

def isNodeTextImage(tag):
    if tag.get('class', None) and isNode.issubset(set(tag['class'])):
        return True
    return False

def getContentChild(tag):
    """Returns true if tag has content as a class"""
    if tag.get('class', None) and 'content' in tag['class']:
        return True
    return False

def getPriceTag(tag):
    if tag.get('class', None) and isPrice.issubset(set(tag['class'])):
        return True
    return False

def getISBNTag(tag):
    if tag.get('class', None) and "field-field-isbn" in tag['class']:
        return True
    return False

def getNextPage(tag: bs4.Tag):
    return tag.name.lower() == K_LIST_ITEM and tag.has_attr('class') and "pager-next" in tag['class']

def getSAPNode(tag: bs4.Tag):
    return tag.name.lower() == 'div' and tag.has_attr("class") and 'item' in tag['class']




total = 0
import subprocess
import platform
import sys
import io
import base64
import pickle
SITE_ROOT = 'https://www.sapeducation.com.au'
def getAllPages(url, soup=None):
    """Gets all url's recusively"""
    ret = [url]
    soup = bs4.BeautifulSoup(getContent(url), parser) if not soup else soup
    nextPage = soup.find(getNextPage)
    if nextPage:
        print(SITE_ROOT + nextPage.a['href'])
        ret.extend(getAllPages(SITE_ROOT + nextPage.a['href']))
    #pickle.dump(ret, open("sites.pkl", 'wb'))
    return ret


parser = 'lxml'


def titleTag(tag):
    return tag.name=="h3" and tag.has_attr("class") and 'title' in tag['class']

def priceTag(tag):
    return tag.name=='div' and tag.has_attr("class") and 'price' in tag['class']

imageSet = {'imagecache','imagecache-product_sap'}
def imageTag(tag):
    return tag.name=='img' and tag.has_attr("class") and imageSet.issubset(set(tag['class']))

def isbnTag(tag):
    return tag.name == 'div' and tag.has_attr("class") and 'isbn' in tag['class']

def pubTag(tag):
    return tag.name == 'div' and tag.has_attr("class") and 'publisher' in tag['class']

count = 1
def readSelectionPage(file, soup=None):
    global count
    soup = bs4.BeautifulSoup(file, parser) if not soup else soup
    # we need title, author, isbn, price and image

    # get all text
    for node in soup.find_all(getSAPNode):
        # get the text and link to more info.
        titleT =  node.find(titleTag).a
        link = SITE_ROOT + titleT['href']
        name = titleT.text
        price = node.find(priceTag).span.text.lstrip("$")

        author, isbn, image = readProductPage(getContent(link))


        c.execute("""INSERT INTO sap (title, authors, isbn, price, image) VALUES (?, ?, ?, ?, ?)""", (name, author, isbn, price, image))
        print("Inserted: %s, isbn: %s, price: %s" % (name, isbn, price))


def readProductPage(file, soup=None):
    """Given the file link returns lots of good stuff !"""
    soup = bs4.BeautifulSoup(file, parser) if not soup else soup
    # get image
    try:
        image = downloadImage(soup.find(imageTag)['src'])
    except:
        image = ""
        print("Error occurred! image", soup)
    # get isbn
    try:
        isbn = soup.find(isbnTag).text.strip()
    except:
        isbn = 136912
        print("ERROR OCCUREd! isbn", soup)
    # get author
    auth = 'Singapore Asia Publishers (SAP)'

    return auth, isbn, image


def saveImageAsBAS64(binaryData):
    return(base64.b64encode(binaryData))

def downloadImage(link):
    """Downloads the image, returning base64 encoded string"""
    return saveImageAsBAS64(getContent(link))


def getContent(url, pause=0.5):
    time.sleep(pause)
    return requests.get(url, headers=fakeReq).content


'''
try:
    file = open("basic.htm")
    readSelectionPage(file)
finally:
    file.close()

'''
#print(readProductPage(open('product.htm')))
#print(saveImageAsBAS64(requests.get("https://www.coroneos.com.au/sites/fivesenseseducation.com.au/files/imagecache/product/giant-book-general-ability-tests-years-5-8-basic-skills-no-176-9781862942868-2194-1316257626b.jpg").content))

import sqlite3
import time
conn = sqlite3.connect("database.db")
c = conn.cursor()

#print(getAllPages("https://www.sapeducation.com.au/category/sap-product-categories/primary-english"))
scrape = "https://www.sapeducation.com.au/category/sap-product-categories/college"
#for iter, i in enumerate(getAllPages("https://www.sapeducation.com.au/category/sap-product-categories/primary-english")):
#for iter, i in enumerate(pickle.load(open("sites.pkl", 'rb'))):
for iter, i in enumerate(getAllPages(scrape)):
    readSelectionPage(getContent(i))
    conn.commit()
    print("commited no: %d" % iter)






