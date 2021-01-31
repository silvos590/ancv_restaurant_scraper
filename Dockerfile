FROM python:3
RUN pip install selenium
RUN pip install lxml
RUN pip install requests
RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add
RUN echo "deb [arch=amd64]  http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
RUN apt-get -y update
RUN apt-get -y install google-chrome-stable
ADD ancv_html_scraper.py /
#ADD https://chromedriver.storage.googleapis.com/LATEST_RELEASE CHROME_LATEST_RELEASE
ADD https://chromedriver.storage.googleapis.com/88.0.4324.96/chromedriver_linux64.zip chromedriver_linux64.zip
RUN unzip chromedriver_linux64.zip 
RUN mv chromedriver /usr/bin/chromedriver
RUN chown root:root /usr/bin/chromedriver
RUN chmod +x /usr/bin/chromedriver
RUN rm chromedriver_linux64.zip
ENTRYPOINT ["python3", "./ancv_html_scraper.py"]