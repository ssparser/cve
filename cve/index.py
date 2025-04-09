import pandas as pd
from collections import defaultdict
import json
from model import get_ai_response
import urllib3
import requests




urllib3.disable_warnings()

df = pd.read_csv('./data.csv')

services = df['Project Name'].value_counts()
total_services = len(services)
urls = []

projects = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

for index, row in df.iterrows():
    library = row["Component Name"]
    version = row["Component Version"]
    cveid = row["CVE ID"]

    service = row["Project Name"]

    projects[service][library][version].append(cveid)  

for service, libraries in projects.items():
    print(f"Service: {service}")
    for library, versions in libraries.items():
        for version, cveids in versions.items():
            print(f"  Library: {library}, Version: {version}, CVE IDs: {cveids}")
 

def getNVD(cveID):
    if cveID == "":
        return {"error": "Empty CVE ID"}
    
    url = "https://services.nvd.nist.gov/rest/json/cves/2.0" 

    payload = {}
    headers = {}

    res = requests.request("GET", url, headers=headers,params={'cveId':cveID}, data=payload,verify=False)
    return res.json()

version = '2.11.0'
cve_data = getNVD('CVE-2024-47554')

question_data = {
    "cve_data": cve_data,
    "affected_version": version
}

question = json.dumps(question_data)
res =  get_ai_response(question)

print(res)




#cveId=CVE-2024-22259