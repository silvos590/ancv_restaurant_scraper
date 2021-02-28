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
  
# Usage via Docker

```
docker build -t ancvrestaurantscraper:latest
docker run -rm -ti ancvrestaurantscraper:latest "-c <city>"
```

Then you can access the generated file by accessing the exited container with a bash console

```
docker commit `docker ps -q -l` ancvrestaurantscraper_output:latest
docker run -it ancvrestaurantscraper_output:latest /bin/bash
```
