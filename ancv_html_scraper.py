from os import makedirs, path
from lxml import html
import requests
import urllib
import getopt, sys


def restoLookup(city, output):
    address = lambda n,city: f'https://guide.ancv.com/recherche/liste/cv?page={n}&rows=30&f%5B0%5D=im_field_ptl_activite_reference%3A6339&f%5B1%5D=im_field_ptl_activite_reference%3A6344&localisation={city}'

    file = open(output,"w")

    print(f'Start...')
    total_resto = 0
    resto_set = set()
    for i in range(8 + 1):
        page = requests.get(address(i,city))
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


    print('Done')
    print(f'Resto found: {len(sorted_set)}')

def usage():
    print('Usage: ./ancv_html_scraper.py -c <city> -o <output-dir>')

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ho:v:c:", ["help", "output=","city="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    output = None
    city = None
    verbose = False
    for o, a in opts:
        if o == "-v":
            verbose = True
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-o", "--output"):
            output = a
        elif o in ("-c", "--city"):
            city = a
        else:
            assert False, "unhandled option"

    if(city == None):
        print('city is a mandatory parameter')
        exit(1)

    if(output == None):
        output = 'restaurants_cv.txt'

    restoLookup(city, output)

if __name__ == "__main__":
    main()
