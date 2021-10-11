# -*- coding: utf-8 -*-
"""
Created on Mon Sep 27 13:50:16 2021

@author: IrisChen
"""


import requests
import time
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

my_timeout = 10
my_delay = 2
my_header = {'user-agent': 'ACSI-app/0.0.1'}
#my_proxy = {'https':'https://127.0.0.1:8080'}

df = pd.read_excel('url_sample.xlsx')
df.columns # set the first row as the name of the column 
urls= df['Targets'] 

titles = ['Targets','Time','Status','Reason']
df2 = pd.DataFrame(columns = titles)

i=0

for url in urls:
    try:
        df2.at[i,'Targets'] = url
        
        t = time.localtime()
       # print(time.asctime())
        df2.at[i,'Time'] = time.asctime()
        
       
        #r = requests.get(url, timeout=my_timeout, headers = my_header, proxies = my_proxy, verify = False)
        r = requests.get(url, timeout=my_timeout, headers = my_header)
        #print(r.url)  
        #print(r.status_code)
        df2.at[i,'Status'] = r.status_code
        #print(r.reason)
        df2.at[i,'Reason'] = r.reason
        
    except requests.exceptions.Timeout as errt:
        df2.at[i,'Status'] = 'Timeout'
        df2.at[i,'Reason'] = errt    
        #print ("Timeout Error:",errt)
    except requests.exceptions.ConnectionError as errc:
        df2.at[i,'Status'] = 'Connection Error'
        df2.at[i,'Reason'] = errc  
        #print ("Error Connecting:",errc)
    except requests.exceptions.RequestException as err:
        df2.at[i,'Status'] = 'Requests Error'
        df2.at[i,'Reason'] = err  
        #print ("OOps: Something Else",err)    
    finally:
        i=i+1
        time.sleep(my_delay)


df2.to_excel('url_sample_results.xlsx',index = False)


df2
