# Launch ancv_restaurant_scraper.py script
Python script to get the list of restaurants accepting chèques vacances

Update: Since new version of the website the restaurants search is much faster, this scripts could still be useful to get once for all the list for your city.

Usage: ./ancv_html_scraper.py -c city -o output-file

# Dependencies
```
pip install selenium
apt-get -y install google-chrome-stable
```
The selenium library is using Chrome as webdriver, so you have to do the following:

1) Install chrome google-chrome-stable
2) Download the chromedriver (check the latest version here -> https://chromedriver.storage.googleapis.com/LATEST_RELEASE)
3) Perform the following steps:

```
unzip chromedriver_linux64.zip 
mv chromedriver /usr/bin/chromedriver
chown root:root /usr/bin/chromedriver
chmod +x /usr/bin/chromedriver
```
  
# Usage as web app via Docker

A Flask simple webapp have been created. To start it build the docker image and run the container:

```
docker build -t ancvrestaurantscraper:latest .
docker run --rm -d ancvrestaurantscraper:latest
```
Then connect to this URL to access the webapp:
```
http://localhost:5000/
```

To create a new image (not needed):

```
docker commit `docker ps -q -l` ancvrestaurantscraper_output:latest
docker run -it ancvrestaurantscraper_output:latest /bin/bash
```
