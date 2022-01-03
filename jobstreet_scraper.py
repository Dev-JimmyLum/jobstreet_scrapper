from os import link
import requests # for web requests
from bs4 import BeautifulSoup # a powerful HTML parser
import pandas as pd # for .csv file read and write
import re # for regular regression handling
import json
import numpy as np
import time
from alive_progress import alive_bar
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'}

def linksByKeys(keys):


    links_dic = dict()

    for key in keys:
 
        links_dic[key] = linksByKey(key)
        print('{} {} positions found!'.format(len(links_dic[key]),key))
    return links_dic

def linksByKey(key):
    ## key: a job role
    ## return: a list of links

    # parameters passed to  http get/post function
    base_url = 'https://www.jobstreet.com.my/en/job-search/job-vacancy.php'
    link_url = 'https://www.jobstreet.com.my/en/job/'
    pay_load = {'key':'','area':1,'option':1,'pg':None,'classified':1,'src':16,'srcr':12}
    pay_load['key'] = key

    # page number
    pn = 1

    position_links = []
    
    loaded = True
    while loaded:
        page_links = []
        print('Loading page {} ...'.format(pn))
        pay_load['pg'] = pn
        r = requests.get(base_url, headers=headers, params=pay_load)
        # print(r)
        # extract position <a> tags
        # time.sleep(0.2)
        soup = BeautifulSoup(r.text,'html.parser')
        links_2 = soup.select('div[data-search-sol-meta]')
        # print(links_2[0]['data-search-sol-meta'])
        for i,item in enumerate(links_2):
            # print(i)
            json_dict = json.loads(links_2[i]['data-search-sol-meta'])['jobId']
            job_id_num = json_dict.split('-')[3]
            actual_link = link_url + job_id_num
            page_links.append(actual_link)
        
        if not len(page_links):
            loaded = False
        else:
            position_links += page_links
            pn += 1
            # loaded = False
    return position_links

def parseLinks(links_dic):
    ## links_dic: a dictionary of links
    ## return: print parsed results to .csv file
    # print(links_dic)
    
    for key in links_dic:
        jobs = []
        with alive_bar(total=len(links_dic[key]), bar='blocks') as bar:
            for link in links_dic[key]:
                bar()
                jobs.append(parseLink(link))

            result = pd.DataFrame(jobs,columns=['job_id','job_title','company_region','salary','company','working_location','experence_requirement'])
            result['job_id'].replace('',np.nan,inplace=True)
            result.dropna(subset=['job_id'],inplace=True)

            file_name = key+'.csv'
            result.to_csv(file_name,index=False)


def parseLink(link):

	other_detail = getJobDetail(link)
	return  other_detail


def getJobDetail(job_href):
   
    r = requests.get(job_href,headers=headers)

    soup = BeautifulSoup(r.text,'html.parser')
    try:
        job_id = job_href
        job_title = soup.select('div > h1')[0].text
        country = "Malaysia"
        # company who posts the position, very often is a recuriter company
        company_name = soup.select('div[data-automation="detailsTitle"] span')[0].text if soup.select('div[data-automation="detailsTitle"] span')[0].text else None
        # years of working experience required
        years_of_experience= checkValidExp(soup.select('div[class="sx2jih0 zcydq832 zcydq8da lm2olz6"] span')[5].text.strip()) if soup.select('div[class="sx2jih0 zcydq832 zcydq8da lm2olz6"] span')[5] else None
        # location of the company
        company_location = soup.select('div[class="sx2jih0 h6p8rp0 h6p8rp3"] span')[0].text if soup.select('div[class="sx2jih0 h6p8rp0 h6p8rp3"] span')[0] else None
        # industry of the company who posts the position, very often is a recuriter company
        job_salary = checkValidSalry(soup.select('div[class="sx2jih0 h6p8rp0 h6p8rp3"] span')[1].text) if soup.select('div[class="sx2jih0 h6p8rp0 h6p8rp3"] span')[1] else None
        return [job_id,job_title,country,job_salary,company_name,company_location,years_of_experience]
    except:
        return []
    
def checkValidSalry(salary):
    if salary.startswith("MY"):
        return salary.replace("\xa0","")
    else:
        return "-"
def checkValidExp(expereince):
    if expereince.endswith("years") or expereince.endswith("year"):
        return expereince
    else:
        return None
def main():

    # a list of job roles to be crawled
    roles = ['Java Developer','Flutter Developer']
    s = requests.session()
    links_dic = linksByKeys(roles)
    parseLinks(links_dic)

if __name__ == '__main__':
	main()
