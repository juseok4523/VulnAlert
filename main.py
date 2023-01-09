import nvdlib
from dotenv import load_dotenv
import os
import requests
import json
import datetime



#main class
class getVuln():
    def __init__(self):
        load_dotenv()
        self.nvdapikey = os.environ.get("NVDAPI")
        self.fulldumpurl = "https://cve.circl.lu/static/circl-cve-search-expanded.json.gz"
        self.datadir = "./data/" 
        
    def get_nvd(self):
        now_kst = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
        # get new cve
        new_cve = self.new_cve_by_nvd(now_kst - datetime.timedelta(days=1))
        #get update cve
        update_cve = self.update_cve_by_nvd(now_kst - datetime.timedelta(days=1))
    
    def new_cve_by_nvd(self, time):
        startdate = time.strftime('%Y-%m-%d 00:00')
        enddate = time.strftime('%Y-%m-%d 23:59')
        res = nvdlib.searchCVE(pubStartDate=startdate, pubEndDate=enddate, key=self.nvdapikey)
        result = {}
        for i in res:
            tmp = {}
            tmp['id'] = i.id
            tmp['assigner'] = i.sourceIdentifier
            tmp['description'] = [x.value if x.lang == 'en' else '' for x in i.descriptions][0]
            tmp['cwe'] = [x.value if x.lang == 'en' else '' for x in i.cwe] #list
            tmp['reference'] = [x.url for x in i.references] #list
            tmp['published'] = i.published
            tmp['lastModified'] = i.lastModified 
            if 'v30score' in i:
                tmp['cvssv3'] = i.v30score #float
            else :
                tmp['cvssv3'] = 0.0
            if 'v2score' in i:
                tmp['cvssv2'] = i.v2score #float
            else:
                tmp['cvssv2'] = 0.0
            result[i.id] = tmp
        return result
            
    def update_cve_by_nvd(self, time):
       startdate = str(time.strftime('%Y-%m-%dT00:00:00'))+'%2b09:00'
       enddate = str(time.strftime('%Y-%m-%dT23:59:59'))+'%2b09:00'
       url = 'https://services.nvd.nist.gov/rest/json/cvehistory/2.0'
       param = {'changeStartDate':startdate, 'changeEndDate':enddate}
       header = {'apikey':self.nvdapikey}
       res = requests.get(url=url, headers=header, params=param)
       result = {}
       for i in res:
           result[i.change.cveId] = i.change.details
       return result

            
        

def main():
    v = getVuln()
    v.get_nvd()
    
if __name__ == "__main__":
    main()