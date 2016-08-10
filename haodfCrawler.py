#-*- encoding: UTF-8 -*-
#---------------------------------import------------------------------------
import requests
import urllib.parse as urlpar
from bs4 import BeautifulSoup
#---------------------------------functions---------------------------------
#parse WebPage to get target links
def webPageGetter(url):
    host='http://www.haodf.com'
    urlParse=urlpar.urlparse(url)
    if urlParse.netloc== '':
        url = ''.join((host, url))
    headers = {'user-agent':'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'}
    try:
        webPage=requests.get(url, headers=headers)
    except:
        print('webpage retrieving failure')
    if webPage.status_code != 200:
        raise Exception("status_code is {}, unable to retrieve pages".format(webPage.status_code))
    parsedPage=BeautifulSoup(webPage.content, 'html.parser')
    return parsedPage 

def getCities(Page):
    cities = Page('div', class_='dis_article_2')[1]
    cityTags = cities('a')
    for city in cityTags:
        name=city.string
        link=city['href']
        yield name, link

def getHospitals(Page):
    hospitals=Page('div', class_='dis_article_2')[2]
    hospTags=hospitals('a')
    for hospital in hospTags:
        name=hospital.string
        link=hospital['href']
        yield name, link

def getPageFromUrl(url):
    Page = webPageGetter(url)
    pageNumbers=Page('div', class_='dis_article_2')[3]
    PageNumberTags=pageNumbers('a')
    for pageNumber in Pages:
        name=pageNumber.string
        try:
            link=pageNumber['href']
        except:
            link=url
        yield name, link

def getPatInfo(Page):
    comments=Page('table', class_='doctorjy')
    for comment in comments:
        patInfo=[]
        for i in range(5,11):
            var=comment('td')[i].text.replace('\n','')
            patInfo.append(var)
        patInfo_str=','.join(patInfo)
        yield patInfo_str

def getComments(Page):
    comments=Pages('td', class_='spacejy')
    for comment in comments:
        patComm = comment.text.strip()
        patComm = ''.join(('评论:',patComm))
        yield patComm



url='http://www.haodf.com/sitemap-tp/p_1'
page = webPageGetter(url)
for city,link in getCities(page):
    print(city,link, sep=':')

