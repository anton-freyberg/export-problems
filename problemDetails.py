# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 18:59:26 2023

@author: anton.freyberg
"""

import requests
import pandas as pd



dynUrl = 'Dynatrace URL, e.g. https://xxx99999.live.dynatrace.com'
dynToken = 'your API token with problems.read scope'
timeframe = '6h'

headers = {
    'Authorization': 'Api-Token {}'.format(dynToken)
}

#header needed for put request
headersPOST = {
    'Authorization': 'Api-Token {}'.format(dynToken),
    'Content-Type': 'text/plain'
}



def getSecurityProblems():
    query = {#'fields': 'evidenceDetails,impactAnalysis',
             'from': 'now-'+timeframe,
             'fields': 'evidenceDetails,impactAnalysis'
             }
    
    req = requests.get ("{}/api/v2/problems".format(dynUrl), params=query,  headers=headers, verify=False)

    print(req.status_code)
    response = req.json()
    problems = response['problems']
    while "nextPageKey" in response:
        #print(response["nextPageKey"])
        query = {"nextPageKey": response["nextPageKey"]}
        req = requests.get("{}/api/v2/problems".format(dynUrl), params=query,  headers=headers, verify=False)
        response = req.json()
        print(req.status_code)
        problems = problems + response["problems"]
    
    
    print(problems)    
    return problems


def writeToFile(problems, filename ):
    df = pd.json_normalize(problems)
    df.to_csv(filename,sep=';', index=False, quotechar="'", encoding='utf-8')

if __name__ =='__main__':
    problems = getSecurityProblems()
    filename = 'problemsDetails.csv'
    writeToFile(problems, filename )
    
    
    
    
    
    
    