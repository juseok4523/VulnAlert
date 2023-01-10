import nvdlib
from dotenv import load_dotenv
import os
import requests
import json
import datetime
import sqlalchemy
from sqlalchemy import create_engine
import pandas as pd
import numpy as np



#main class
class getVuln():
    def __init__(self, user, passwd, address, dbname, tablename):
        load_dotenv()
        self.nvdapikey = os.environ.get("NVDAPI")
        self.datadir = "./data/" 
        self.nvd_df, self.cpe_df = self.sql_init(user, passwd, address, dbname, tablename)
    
    def sql_init(self, user, passwd, address, dbname):
        try: 
            nvd_df = pd.read_sql_table('NVD', f'mysql+pymysql://{user}:{passwd}@{address}/{dbname}')
            cpe_df = pd.read_sql_table('CPE', f'mysql+pymysql://{user}:{passwd}@{address}/{dbname}')
            return nvd_df, cpe_df
        except Exception as e:
            print(e)
            
    def get_nvd(self):
        now_kst = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
        # get new cve
        new_cve = self.new_cve_by_nvd(now_kst - datetime.timedelta(days=1))
        #get update cve
        update_cve = self.update_cve_by_nvd(now_kst - datetime.timedelta(days=1))
        self.update_db(new_cve, update_cve)
  
    
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
            tmp['cwe'] = [x.value if x.lang == 'en' else '' for x in i.cwe] if 'cwe' in i else [] #list
            tmp['reference'] = [x.url for x in i.references] #list
            tmp['published'] = i.published
            tmp['lastModified'] = i.lastModified
            tmp['cpe'] = i.cpe if 'cpe' in i else '' #list
            tmp['cvssv3'] = i.v30score if 'v30score' in i else 0.0 #float
            tmp['cvssv2'] = i.v2score if 'v2score' in i else 0.0 #float
            result[i.id] = tmp
        return result
            
    def update_cve_by_nvd(self, time):
       startdate = str(time.strftime('%Y-%m-%dT00:00:00'))+'%2b09:00'
       enddate = str(time.strftime('%Y-%m-%dT23:59:59'))+'%2b09:00'
       url = 'https://services.nvd.nist.gov/rest/json/cvehistory/2.0'
       param = {'changeStartDate':startdate, 'changeEndDate':enddate}
       stringParams = '&'.join([k if v is None else f"{k}={v}" for k, v in param.items()])
       header = {'apikey':self.nvdapikey}
       res = requests.get(url=url, headers=header, params=stringParams).json()
       result = {}
       for i in res['cveChanges']:
           result[i['change']['cveId']] = i['change']['details']
       return result

    def update_db(self, new_nvd, update_nvd):
        
        

def main():
    v = getVuln()
    v.get_nvd()
    
if __name__ == "__main__":
    main()