import requests, sys, os
import pdb, sqlite3 
from bs4 import BeautifulSoup

baseURL = "https://remote.co/remote-jobs/"

jobBuckets = ["accounting", "customer service", "online-data-entry", "design",
              "developer", "online-editing", "healthcare", "recruiter", "legal",
              "marketing", "project-manager", "qa", "sales", "virtual-assistant",
              "writing", "other"]

def connectSite(job: str) -> BeautifulSoup:
    currentURL = baseURL + job + "/"
    currentPage = requests.get(currentURL)
    currentHTMLSoup = BeautifulSoup(currentPage.content, "html.parser")
    return currentHTMLSoup

def parseIntialLandingSoup(currentSoup: BeautifulSoup, tagSearch: str) -> BeautifulSoup:
    card_BodyClass = currentSoup.find("div", class_="card bg-light mb-3 rounded-0")
    job_HTML = card_BodyClass.find_all("a", class_="card m-0 border-left-0 border-right-0 border-top-0 border-bottom")

    #

    for job in job_HTML:
        job_Tag = job.find("span", class_="badge badge-success")
        if (type(job_Tag) == type(None)):
            continue; 
        if(job_Tag.text.strip() == tagSearch):
            actualJobPageURL = requests.get("https://remote.co" + job["href"])
            actualJobPageHTMLSoup = BeautifulSoup(actualJobPageURL.content, "html.parser")
            return actualJobPageHTMLSoup
    return None

def parseJobPostingSoup(JobSiteSoup: BeautifulSoup) -> dict:
    jobInfo = {
        "Job Name" : "",
        "Job Location" : "", 
        "Job Posted Date": "",
        "Job Salary": "", 
        "Company Link": "",
        "Apply Link": ""
    }

    #pdb.set_trace()

    #Traversing through the general site:
    job_Name = JobSiteSoup.find("h1", class_="font-weight-bold")
    company_Link = JobSiteSoup.find("div", class_="links_sm")
    if(company_Link is not None):
        company_Link = company_Link.a["href"]
    else:
        company_Link = "N/A"
    job_info_container = JobSiteSoup.find("div", class_="job_info_container_sm")
    apply_Link = JobSiteSoup.find("div", class_="application")
    if(apply_Link is not None):
        apply_Link = apply_Link.a["href"]
    else:
        apply_Link = "N/A"

    #Create a job_info_container for the small nibs of info at the top
    job_Location = job_info_container.find("div", class_="location_sm row")
    job_Posted_Date = job_info_container.find("time")
    if(job_Posted_Date is not None):
        job_Posted_Date = job_Posted_Date["datetime"]
    else:
        job_Posted_Date = "N/A"
    job_Salary = job_info_container.find("div", class_="salary_sm row")

    #Add everything to the jobInfo dictionary
    jobInfo["Job Name"] = job_Name
    jobInfo["Job Location"] = job_Location
    jobInfo["Job Posted Date"] = job_Posted_Date
    jobInfo["Job Salary"] = job_Salary
    jobInfo["Company Link"] = company_Link
    jobInfo["Apply Link"] = apply_Link

    return jobInfo

def writeToDatabase(jobInfo: dict): 

    dataBaseConnection = sqlite3.connect("scrappedData.db")
    cursor = dataBaseConnection.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scrape

            ( 
              Name TEXT,
              Location TEXT,  
              Posted_Date TEXT,
              Salary TEXT,
              Company_Link TEXT,
              Apply_Link TEXT

            )    
    
    ''')
    dataBaseConnection.commit()

    for key in jobInfo:
        if( (jobInfo[key] is None) or (type(jobInfo[key]) == str) ):
            continue
        else:
            jobInfo[key] = jobInfo[key].text

    cursor.execute('''

        INSERT INTO scrape (Name, Location, Posted_Date, Salary, Company_Link, Apply_Link)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (jobInfo["Job Name"], jobInfo["Job Location"], jobInfo["Job Posted Date"], jobInfo["Job Salary"], jobInfo["Company Link"], jobInfo["Apply Link"]))
    
    dataBaseConnection.commit()
    dataBaseConnection.close()

'''def readAndCompare(jobInfo: dict, csv_File: str):

    with open(csv_File, 'r') as currentFile:
        csv_Reader = csv.DictReader(currentFile)

        for row in csv_Reader:
           print(row)      ''' 


def main():
    for job in jobBuckets:
        #
        htmlSoup = connectSite(job)

        jobPageSoup = parseIntialLandingSoup(htmlSoup, str(sys.argv[1]))

        jobInfoDict = None

        if(jobPageSoup == None):
            continue
        else: 
            jobInfoDict = parseJobPostingSoup(jobPageSoup)

        if(jobInfoDict == None):
            continue
        else:
            writeToDatabase(jobInfoDict)



if __name__ == "__main__":
    main()


