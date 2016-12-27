import bs4
fakeReq = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
import requests
import lxml
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

isGoogleImage = {
    'rg_ic',
    'rg_i',
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


def getGoogleImage(tag):
    if tag.get("class", None) and isGoogleImage.issubset(set(tag['class'])):
        return True
    return False


total = 0
import subprocess
import platform
import sys
import io
import base64

sys.setrecursionlimit(2500)

parser = 'lxml'

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
conn = sqlite3.connect("database.db")
c = conn.cursor()
print('https://www.googleapis.com/customsearch/v1?key=%s&cx=%s&q=%s&searchType=image&imgSize=medium&alt=json&num=3' % ('AIzaSyB7O9gMg2Y-Scm6U8wuxae49O2aoXsfKg0',
                                                                                                                          '004069732376962236449:ec49e6ukhpm', '9781742152127',
                                                                                                                      ))

import pickle
import datetime
import json
#pickle.dump(requests.get('https://www.googleapis.com/customsearch/v1?key=%s&cx=%s&q=%s&searchType=image&imgSize=large&alt=json&num=3' % ('AIzaSyB7O9gMg2Y-Scm6U8wuxae49O2aoXsfKg0',
#                                                                                                                      '004069732376962236449:ec49e6ukhpm', '9781742152127',
#


skip = pickle.load(open('skip.pkl', 'rb'))
import pprint
key = 'AIzaSyAjDFgm5_NXHY3yuofstFw7XLSKguJ8Jlg	'
engine = '004069732376962236449:ec49e6ukhpm'

#key = 'AIzaSyA9WnCl_PFSDDWrKrHmySfiA_bj4P0bS94'

#key = 'AIzaSyBOSgJ5HCsYw_Sap-RmTXjOo8G11CKyRSs'
#key = 'AIzaSyCKeyr-7d-rg65nTmHUky7LJ4PGhpDP2_Q'
counter = 0

for i in c.execute("""SELECT * FROM excel WHERE image IS NULL""").fetchall():
    title, auth, isbn, f,b,price, image = i

    if str(isbn) in skip:
        print("Skipping,", isbn)
        continue

    js = json.loads(requests.get('''https://www.googleapis.com/customsearch/v1?key=%s&cx=%s&q=%s&searchType=image&imgSize=medium&alt=json&num=3'''
                                 % (key,engine, isbn), headers=fakeReq).text)
    print("DOING %s:%s" %(isbn, title))
    try:
        js=js['items'][0]
        print(js['link'])
        #c.execute("""UPDATE basic SET image=? WHERE isbn=?""", (downloadImage(js['link']), isbn) )

    except:
        try:
            if js['queries']['request'][0]['totalResults'] == 0 or js['queries']['request'][0]['totalResults'] == '0':
                # no images for some reason, add to skip
                skip.add(str(isbn))
                print('skip=', skip)
                pickle.dump(skip, open("skip.pkl", 'wb'))

            else:
                pprint.pprint(js)
                raise

        except:
            pprint.pprint(js)
            raise

    counter += 1
    print(counter, 'amount used')

    conn.commit()
    time.sleep(4)

