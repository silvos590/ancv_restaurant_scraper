# Launch ancv_restaurant_scraper.py script
Python script to get the list of restaurants accepting chèques vacances

Usage: ./ancv_html_scraper.py -c city -o output-file
  
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
