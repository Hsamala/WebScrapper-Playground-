import requests 
import re
#import pdb; pdb.set_trace()
from bs4 import BeautifulSoup



URL = "https://realpython.github.io/fake-jobs/"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

job_elements = soup.find_all(string=lambda text: "python" in text.lower(), class_="title is-5")
actual_Python_Jobs_HTML = [job_element.parent.parent.parent.parent for job_element in job_elements]

for job in actual_Python_Jobs_HTML:
    job_Name = job.find("h2", class_="title is-5")
    job_Location = job.find("p", class_="location")
    job_Company = job.find("h3", class_="subtitle is-6 company")
    html_Regex = re.compile(r'.html')
    apply_Link = job.find("a", class_="card-footer-item", href=html_Regex)
    print(job_Name.text.strip())
    print(job_Company.text.strip())
    print(job_Location.text.strip())
    print(apply_Link.get("href").strip())
    print()