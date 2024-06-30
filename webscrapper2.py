import requests, sys
import pdb
from bs4 import BeautifulSoup

baseURL = "https://remote.co/remote-jobs/"

jobBuckets = ["accounting", "customer service", "online-data-entry", "design",
              "developer", "online-editing", "healthcare", "recruiter", "legal",
              "marketing", "project-manager", "qa", "sales", "virtual-assistant",
              "writing", "other"]

def connectSite(job: str):
    currentURL = baseURL + job + "/"
    currentPage = requests.get(currentURL)
    currentHTMLSoup = BeautifulSoup(currentPage.content, "html.parser")
    return currentHTMLSoup

def parseIntialLandingSoup(currentSoup: BeautifulSoup, tagSearch: str):
    card_BodyClass = currentSoup.find("div", class_="card bg-light mb-3 rounded-0")
    job_HTML = card_BodyClass.find_all("a", class_="card m-0 border-left-0 border-right-0 border-top-0 border-bottom")

    for job in job_HTML:
        job_Tag = job.find("span", class_="badge badge-success")
        if(job_Tag.text.strip() == tagSearch):
            actualJobPageURL = requests.get("https://remote.co" + job["href"])
            actualJobPageHTMLSoup = BeautifulSoup(actualJobPageURL.content, "html.parser")
            return actualJobPageHTMLSoup
    return None

def parseJobPostingSoup(JobSiteSoup: BeautifulSoup):
    jobInfo = []
    #Traversing through the general site:
    job_Name = JobSiteSoup.find("h1", class_="font-weight-bold")
    company_Link = JobSiteSoup.find("div", class_="links_sm").a["href"]
    job_info_container = JobSiteSoup.find("div", class_="job_info_container_sm")
    apply_Link = JobSiteSoup.find("div", class_="application").a["href"]

    #Create a job_info_container for the small nibs of info at the top
    job_Location = job_info_container.find("div", class_="location_sm row")
    job_Posted_Date = job_info_container.find("time")["datetime"]
    job_Salary = job_info_container.find("div", class_="salary_sm row")

    #Add everything to the job List
    jobInfo.append(job_Name)
    jobInfo.append(job_Location)
    jobInfo.append(job_Posted_Date) 
    jobInfo.append(job_Salary)
    jobInfo.append(company_Link)
    jobInfo.append(apply_Link)

    for item in jobInfo:
        if(item == None):
            continue
        elif(type(item) == str):
            print(item)
        else:
            print(item.text.strip())

    print('---------------------------------------------------------------------')

def main():
    for job in jobBuckets:
        #pdb.set_trace()
        htmlSoup = connectSite(job)
        jobPageSoup = parseIntialLandingSoup(htmlSoup, str(sys.argv[1]))
        if(jobPageSoup == None):
            continue
        else: 
            parseJobPostingSoup(jobPageSoup)
    

if __name__ == "__main__":
    main()


