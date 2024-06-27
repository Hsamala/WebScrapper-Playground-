import requests
import pdb; pdb.set_trace()
from bs4 import BeautifulSoup

baseURL = "https://remote.co/remote-jobs/"

jobBuckets = ["accounting", "customer service", "online-data-entry", "design",
              "developer", "online-editing", "healthcare", "recruiter", "legal",
              "marketing", "project-manager", "qa", "sales", "virtual-assistant",
              "writing", "other"]

def scrapeSite(job):
    currentURL = baseURL + job + "/"
    currentPage = requests.get(currentURL)
    currentHTMLSoup = BeautifulSoup(currentPage, "html.parser")
    print(currentHTMLSoup.find("title"))

for job in jobBuckets:
    scrapeSite(job)


    



