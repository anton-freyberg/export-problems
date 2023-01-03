# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 18:59:26 2023

@author: anton.freyberg
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 15:41:41 2022

@author: anton.freyberg
"""

import  dateutil
from os import environ
import json
import requests
import numpy as np
import pandas as pd
import datetime, time
import pytz
from dateutil.relativedelta import relativedelta
import re
from os import environ
import requests
import numpy as np
import datetime
import calendar
import  dateutil
import pandas as pd
import sys
import pytz
import re


#dynToken = environ.get('DYN_API_TOKEN')
#dynUrl = environ.get('DYN_API_URL')

dynUrl = ''
dynToken = ''
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
    
    
    
    
    
    
    