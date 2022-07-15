# import requests
#
# URL = "https://www.flipkart.com/"
# page = requests.get(URL)
#
# print(page.text)

import requests
from bs4 import BeautifulSoup

URL = "https://realpython.github.io/fake-jobs/"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(id="ResultsContainer")
job_elements = results.find_all(class_="card-content")

print(results.prettify())