import bs4
import urllib.request
import requests
isNode = {'node',
             'node-teaser',
             'node-product-book',
             'node-product-book-teaser',
             'node-product',
             'node-product-teaser',
             'clear-block'
          }

class OutOfHTMLException(Exception):
    """OUCH! you've run out of html to parse...."""
    ...

def isNodeTextImage(tag):
    if tag.get('class', None) and isNode.issubset(set(tag['class'])):
        return True
    return False

def getContentChild(tag):
    """Returns true if tag has content as a class"""
    if tag.get('class', None) and 'content' in tag['class']:
        return True
    return False
total = 0
import subprocess
import platform
import sys



with open("basic.htm") as f:
    soup = bs4.BeautifulSoup(f,'html.parser')
    # get all text&image nodes

    for link in soup.find_all(isNodeTextImage):
        # get the text and link
        a_tag = (link.find(getContentChild)).find('a')
        book_name = a_tag['title']
        book_link = a_tag['href']
        print(book_name)
        '''
        if link.get('class', None):
            #print(link['class'])
            if isNode.issubset(set(link['class'])):
                print(set(link['class']), isNode.issubset(set(link['class'])))
                total += 1
                '''
