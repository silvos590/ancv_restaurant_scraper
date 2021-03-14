from os import makedirs, path
from lxml import html
import requests
import urllib
import getopt, sys, os
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

#old_address = lambda n,city: f'https://guide.ancv.com/recherche/liste/cv?page={n}&rows=30&f%5B0%5D=im_field_ptl_activite_reference%3A6339&f%5B1%5D=im_field_ptl_activite_reference%3A6344&localisation={city}'
address = lambda city: f'https://leguide.ancv.com/ptl/recherche/list?location={city}&filters%5Bdomaine_activite_principale%5D%5BRestauration%5D=Restauration'

# Write the list of sorted items in file
def store(set_items, output):
    if output == None:
        print('output name is mandatory')
        exit(1)
    else:
        with open(output,"w") as file:
            for t in set_items:
                str =  ''.join(t)
                file.writelines(str + '\n')

def getTotalNumberOfRestaurants(browser, city):
    # Get the total number of restaurants
    page = requests.get(address(city))
    browser.get(address(city))
    if page.status_code != 200:
        print(f'cannot connect to ancv website')
        sys.exit(1)

    tree = html.fromstring(page.content)
    total_resto_number = tree.xpath('//*[@id="spanNbResult"]/text()')
    if total_resto_number == None or len(total_resto_number) == 0:
        return 0
    else:
        print(f'Total number of restaurants: {total_resto_number[0]}')

    return int(total_resto_number[0])

def restoLookup(city):
    print('Start...')
    total_resto = 0
    resto_set = set()

     # Set option to do not open the browser
    options = Options()
    options.add_argument('--headless')
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    browser = webdriver.Chrome(options=options)

    # total restaurants
    total_resto = getTotalNumberOfRestaurants(browser, city)
    if total_resto == 0:
        print(f'no restaurant found')
        return

    # collect all the restaurants name
    restaurants = []

    # With the latest version of the site, the list of restaurants is loaded dinamically
    # when the user scrolls the page, this made their website much more usable.
    # The infinite scroll can be normally stop when the scrolled more than remain scrollHeight
    # for some reason in this website thescrollHeight attribute is not updated after each scroll.
    # The workaround was to stop the loop we found all the restaurants.
    # I will add a safety timer to avoid infinite loop.

    time.sleep(2)  # Allow 2 seconds for the web page to open
    scroll_pause_time = 4 # set pause time between scrolls
    screen_height = browser.execute_script("return window.screen.height;") # get the screen height of the web
    i = 1
    
    while True:
        # scroll one screen height each time
        browser.execute_script("window.scrollTo(0, {screen_height}*{i}*10);".format(screen_height=screen_height, i=i))  
        i += 1
        time.sleep(scroll_pause_time)
        # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
        #scroll_height = browser.execute_script("return document.body.scrollHeight;")  

        restaurants = browser.find_elements_by_xpath('//*[@id="ptl-list-content"]/div/div/div[2]/p[2]')

        print(f'resto found till now: {len(restaurants)}')
        # Break the loop when the height we need to scroll to is larger than the total scroll height
        #if (screen_height) * i > scroll_height:
        # Warning: stopping when we found all the restaturants
        if len(restaurants) >= total_resto:
            break 
    
    if len(restaurants) == 0:
        print(f'no restaurant found')
        return
    else:
        print(f'restaurants {len(restaurants)} found')
    
    # Add restaurants to the set
    for r in restaurants:
        print(f'Restaurant name: {r.text}')
        t = r.text.replace("\'", "")
        resto_set.add(t)

    print('Removing duplicates and sorting the results...')
    sorted_set = sorted(resto_set)

    print('Done')
    print(f'Restaurants found: {len(sorted_set)}')
    return sorted_set

def usage():
    print('Usage: ./ancv_html_scraper.py -c <city> -o <output-file>')

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ho:v:c:s", ["help", "output=", "city=", "silent-mode"])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    output = None
    city = None
    verbose = False
    silent_mode = False
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
        elif o in ("-s", "--silent-mode"):
            silent_mode = True
        else:
            assert False, "unhandled option"

    if silent_mode == True:
        f = open(os.devnull, 'w')
        sys.stdout = f

    if city == None :
        print('city is a mandatory parameter')
        exit(1)

    if output == None :
        output = 'restaurants_cv.txt'

    restaurants = restoLookup(city)

    store(restaurants, output)

if __name__ == "__main__":
    main()
