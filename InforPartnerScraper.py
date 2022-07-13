#Infor Partner Web Scraper

import requests
from bs4 import BeautifulSoup as bs
import csv
import re

URL = 'https://partners.infor.com/?ch=true&al=true&na=true&page='
URL_PartDet = 'https://partners.infor.com/Search/PartnerDetails/'
lines_list=[]

for page in range(1, 19):
 
    req = requests.get(URL + str(page))
    soup = bs(req.text, 'html.parser')
    lines = soup.find('div', id="results").find_all('h2')    

    for i in range(0, 10):

        d={} 

        if page >1:
            d['Partner Number']=(1+(i)+page*10)
        else:
            d['Partner Number']=i+1
        d['Partner Name']=re.sub(r'[^\x00-\x7f]', "",lines[i].text)
        lines_dataid= re.findall('"(.*)"', str(lines[i]))

        # Company Details URL request
        req_CompanyDetails=requests.get(URL_PartDet + str(lines_dataid).replace("'","").replace("[","").replace("]",""))
        soup_CompanyDetails = bs(req_CompanyDetails.text, 'html.parser')
        company_url = soup_CompanyDetails.find('a').text
        
        d['Partner URL']= company_url
        ul_details= str(soup_CompanyDetails.find_all('ul')[0]).replace("\n","").replace("<li>","").replace("</li>"," -").replace("<ul>","").replace("</ul>","").rstrip('-')
        d['Infor Products'] = ul_details
        ul_InterestArea = str(soup_CompanyDetails.find_all('ul')[1]).replace("\n","").replace("<li>","").replace("</li>"," -").replace("<ul>","").replace("</ul>","").rstrip('-')
        d['Areas of Interest'] = ul_InterestArea
        ul_Industry = str(soup_CompanyDetails.find_all('ul')[2]).replace("\n","").replace("<li>","").replace("</li>"," -").replace("<ul>","").replace("</ul>","").rstrip('-')
        d['Industry and Microvertical'] = ul_Industry

        lines_list.append(d.copy())

filename = 'Infor Partners Details.csv'
with open(filename, 'w', newline='') as f:
    w = csv.DictWriter(f,['Partner Number','Partner Name','Partner URL' ,'Infor Products', 'Areas of Interest','Industry and Microvertical'])
    w.writeheader()
    w.writerows(lines_list)