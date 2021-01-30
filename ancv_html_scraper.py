from os import makedirs, path
from lxml import html
import requests
import urllib
import sys

# CHANGE THIS PATH TO YOUR OWN
FILE_PATH = '/home/aldo/scripts/restaurant_cv.txt'

address = lambda n: f'https://guide.ancv.com/recherche/liste/cv?page={n}&rows=30&f%5B0%5D=im_field_ptl_activite_reference%3A6339&f%5B1%5D=im_field_ptl_activite_reference%3A6344&localisation=Nice&coordinate=43.70025000000004%2C7.277740000000051'

file = open(FILE_PATH,"w")

print(f'Start...')
total_resto = 0
resto_set = set()
for i in range(8 + 1):
    page = requests.get(address(i))
    print(f'page {i} found')
    tree = html.fromstring(page.content)
    #filenames = tree.xpath('//a[@class="title"]/attribute::href')
    titles = tree.xpath('//div[@class="field-item even"]/a/h2/text()')
    #print(titles)
    for t in zip(titles):
        #t = t.replace('/','_')
        total_resto += 1
        print(f'Restaurants found n. {total_resto}! {t}') # py3
        resto_set.add(t)

sorted_set = sorted(resto_set)

for t in sorted_set:
    str =  ''.join(t)
    file.writelines(str + '\n')


print(f'Done')
print(f'Resto found: {len(sorted_set)}')
