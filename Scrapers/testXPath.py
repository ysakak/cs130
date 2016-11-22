import csv
import os
from multiprocessing.dummy import Pool as ThreadPool
import re
import string
import sys
import requests
from lxml import html


def get_page(url):
	page = requests.get(url)
	return page

def get_if_exists(l, index):
    if len(l) <= index or index < 0:
        return ""
    else:
        return l[index]

page = get_page("http://www.bruinwalk.com/search/?sort=alphabetical&category=classes&page=1")
tree = html.fromstring(page.content)
x = tree.xpath("/html/body/section/div/section/div[2]/div[2]/div[4]/div[5]/div/div[1]/span/b")
print x 
y = get_if_exists(x, 0)
print y
