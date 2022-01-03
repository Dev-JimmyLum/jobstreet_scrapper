## JobStreet Scraper

A python scraper to extract the certain available job information from the jobstreet platform

Please ensure all the required packages has been installed before running the script.

## Packages

```
pip install requests

pip install BeautifulSoup

pip install pandas

pip install numpy

pip install alive_progress
```

## Run the scraper

Before running please ensure you are already setup the configuration

```python
##job_street_scraper.py
## Configuration (Please change the position role you want to crawl)
roles = ['Java Developer','Flutter Developer']
## To crawl other than Malaysia region user may have to change the internet country code below
base_url = 'https://www.jobstreet.com.my/en/job-search/job-vacancy.php'
link_url = 'https://www.jobstreet.com.my/en/job/'
```

```
python jobstreet_scraper.py
```
