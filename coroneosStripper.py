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


total = 0
import subprocess
import platform
import sys
import io
import base64

parser = 'html.parser'
def readSelectionPage(file, soup=None):
    soup = bs4.BeautifulSoup(file, parser) if not soup else soup
    # we need title, author, isbn, price and image

    # get all text
    for link in soup.find_all(isNodeTextImage):
        # get the text and link to more info.
        a_tag = (link.find(getContentChild)).find('a')
        book_name = a_tag['title']
        book_link = "https://www.coroneos.com.au" + a_tag['href']
        yield (book_name, *readProductPage(getContent(book_link))) #name, price, image, author, isbn


def readProductPage(file, soup=None):
    """Given the file link returns lots of good stuff !"""
    soup = bs4.BeautifulSoup(file, parser) if not soup else soup
    # get prices
    price = soup.find(getPriceTag).string.lstrip('$')
    # get image

    # get author
    author = soup.find(getAuthor).string.strip()
    # get isbn
    isbn = soup.find(getISBNTag).div.div.string.strip()
    try:
        image = getContent(soup.find(getMainProductImage).a['href'])
    except AttributeError:
        image = ''
        print("ERROR ON ", isbn)
        return (price, None, author, isbn)

    return (price, saveImageAsBAS64(image), author, isbn)

def saveImageAsBAS64(binaryData):
    return(base64.b64encode(binaryData))

def downloadImage(link):
    """Downloads the image, returning base64 encoded string"""
    return saveImageAsBAS64(getContent(link))


def getContent(url):
    return requests.get(url, headers=fakeReq).content
import re
basic1 = re.compile(r'\(.*[0-9]+.*\)')
basic2 = re.compile(r'#.+?$')
numberRE = re.compile(r'[0-9]+[A|B]?\)')

def GetID(titleISBN):
    # define id, title, isbn
    title, isbn = titleISBN

    number = (basic1.findall(titleISBN[0]))
    if not number:
        # use regex 2
        number = basic2.findall(titleISBN[0])
        if not number:
            print(title,isbn)
            id = input("Enter BASIC ID, Enter to cancel: ")
            if not id:
                return None
            return id
        else:
            return number[0].lstrip("#")

    else:
        # it is good! use regex 1 (Name No.Number)
        number = number[0] # first element is ppropert
        return numberRE.search(number).group(0)[:-1]

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
conn = sqlite3.connect("basicSkills.db")
c = conn.cursor()


while True:
    x = input("Enter url of page: ")
    for i in readSelectionPage(getContent(x)):
        print(i[0:2], i[3:])
        id = (GetID((i[0],i[4])),)
        c.execute("""INSERT INTO basic
                    (title, price, image, authors, isbn, id) VALUES
                    (?,?,?,?,?,?)""", i + id)
        print(id)
        time.sleep(4)

    conn.commit()
    break








