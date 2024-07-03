import requests, sys, os
import pdb, csv
from bs4 import BeautifulSoup

newJson = "new_scrapped_data.csv"

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

    for job in job_HTML:
        job_Tag = job.find("span", class_="badge badge-success")
        if(job_Tag.text.strip() == tagSearch):
            actualJobPageURL = requests.get("https://remote.co" + job["href"])
            actualJobPageHTMLSoup = BeautifulSoup(actualJobPageURL.content, "html.parser")
            return actualJobPageHTMLSoup
    return None

def parseJobPostingSoup(JobSiteSoup: BeautifulSoup) -> list:
    jobInfo = {
        "Job Name" : "",
        "Job Location" : "", 
        "Job Posted Date": "",
        "Job Salary": "", 
        "Company Link": "",
        "Apply Link": ""
    }
    #Traversing through the general site:
    job_Name = JobSiteSoup.find("h1", class_="font-weight-bold")
    company_Link = JobSiteSoup.find("div", class_="links_sm").a["href"]
    job_info_container = JobSiteSoup.find("div", class_="job_info_container_sm")
    apply_Link = JobSiteSoup.find("div", class_="application").a["href"]

    #Create a job_info_container for the small nibs of info at the top
    job_Location = job_info_container.find("div", class_="location_sm row")
    job_Posted_Date = job_info_container.find("time")["datetime"]
    job_Salary = job_info_container.find("div", class_="salary_sm row")

    #Add everything to the jobInfo dictionary
    jobInfo["Job Name"] = job_Name
    jobInfo["Job Location"] = job_Location
    jobInfo["Job Posted Date"] = job_Posted_Date 
    jobInfo["Job Salary"] = job_Salary
    jobInfo["Company Link"] = company_Link
    jobInfo["Apply Link"] = apply_Link

    return jobInfo

def writeToCSV(jobInfo: dict, csv_File: str):

    for key in jobInfo:
        if( type(jobInfo[key]) == str):
            jobInfo[key] = jobInfo[key]
        elif ( jobInfo[key] == None):
            jobInfo[key] = "None"
        else:
            jobInfo[key] = str(jobInfo[key].text.strip())
    
    write_file_size = os.path.getsize(newJson)

    if(write_file_size == 0): 
        with open(csv_File, "w", newline="") as csv_file:
            csv_writer = csv.writer(csv_file)
        
            for key, value in jobInfo.items():
                csv_writer.writerow([key, value])
    else:
       with open(csv_File, "a", newline="") as csv_file:
            csv_writer = csv.writer(csv_file)
        
            for key, value in jobInfo.items():
                csv_writer.writerow([key, value]) 


def readAndCompare(jobInfo: dict, csv_File: str):

    with open(csv_File, 'r') as currentFile:
        csv_Reader = csv.DictReader(currentFile)

        for row in csv_Reader:
           print(row)       


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
            writeToCSV(jobInfoDict, newJson)

        readAndCompare(jobInfoDict, newJson)



if __name__ == "__main__":
    main()


