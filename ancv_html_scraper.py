from os import makedirs, path
from lxml import html
import requests
import urllib
import getopt, sys
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def restoLookup(city, output):
    address = lambda n,city: f'https://guide.ancv.com/recherche/liste/cv?page={n}&rows=30&f%5B0%5D=im_field_ptl_activite_reference%3A6339&f%5B1%5D=im_field_ptl_activite_reference%3A6344&localisation={city}'

    file = open(output,"w")

    print('Start...')
    total_resto = 0
    resto_set = set()

    # Get the number of pages for the choosen city
    # tree.xpath doesn't get the span text for an unknown reason, had to use selenium
    # pager_count = tree.xpath("//div[@id='pager1']/span/text()")

    # Set option to do not open the browser
    options = Options()
    options.add_argument('--headless')

    browser = webdriver.Chrome(options=options)
    browser.get(address(1,city))
    pager_count = browser.find_elements_by_xpath('.//span[@class="pager-count"]')

    if len(pager_count) == 0:
        print("Cannot find number of pages")
        sys.exit()

    # e.g.: '1 - 2'
    x = re.search("([0-9].*)( - )([0-9].*)", pager_count[0].text)
    totalpages = x[3]
    print('Number of pages', totalpages)

    for i in range(int(totalpages)):
        page = requests.get(address(i,city))

        if(page.status_code != 200):
            break

        tree = html.fromstring(page.content)
        titles = tree.xpath('//div[@class="field-item even"]/a/h2/text()')

        if len(titles) == 0:
            break
        else:
            print(f'page {i} found')

        for t in titles:
            #t = t.replace('/','_')
            total_resto += 1
            print(f'Restaurants found n. {total_resto}! {t}')
            resto_set.add(t)

    sorted_set = sorted(resto_set)

    # Write the list of restaurant in file
    for t in sorted_set:
        str =  ''.join(t)
        file.writelines(str + '\n')

    print('Done')
    print(f'Resto found: {len(sorted_set)}')

def usage():
    print('Usage: ./ancv_html_scraper.py -c <city> -o <output-file>')

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
