from bs4 import BeautifulSoup
import urllib2
from core.models import Event

def get_page_content(url):
    req = urllib2.Request(url,
                          headers = {"Referer": "http://www.baidu.com",
                                     "User-Agent": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.68 Safari/534.24"
                                     })
    html = urllib2.urlopen(url = req, timeout = 10).read()
    return html.decode('utf-8')

def get_page_href(html):
    hrefs = {}
    soup = BeautifulSoup(html)
    for link in soup.findAll('a'):
        href = link.get('href')
        if (href != None):
            hrefs[href] = 1
    return hrefs.keys()

def crawlEventBrite(url):
    html = get_page_content(url)
    soup = BeautifulSoup(html)
    name = soup.find("div", {"id" : "event_header"}).find("span", {"class" : "summary"}).text.strip()
    address = soup.find("span", {"class" : "street-address"}).text.strip()
    location = soup.find("span", {"class" : "locality" }).text.strip()
    region = soup.find("span", {"class" : "region" }).text.strip()
    start_time = soup.find("span", {"class" : "dtstart" }).find("span", {"class" : "value-title"})['title'].strip()
    start_time = start_time.split('T')
    start_date = start_time[0]
    start_time = start_time[1]
    end_time = soup.find("span", {"class" : "dtend" }).find("span", {"class" : "value-title"})['title'].strip()
    end_time = end_time.split('T')
    end_date = end_time[0]
    end_time = end_time[1]

    event, created = Event.objects.get_or_create(name=name, address_line1=address,
                                 category='GE',
                                 address_line2=' ',
                                 city=location,
                                 state=region, start_time=start_time,
                                 end_time=end_time, start_date=start_date,
                                 end_date=end_date, URL=url)
    return event

def test():
    url = 'https://foundersspacesvsept2013.eventbrite.com/'
    crawEventBrite(url)
