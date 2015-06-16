# Duplicate of the script that Alex and Dale created: https://github.com/akmiller01/alexm-util/blob/master/DevInit/scrape_google_group.py

# TO DO:
# - Scrape date and time for each message
# - Remove preview text for each message


import time
import pdb
from optparse import OptionParser
from lxml.html import fromstring
from selenium import webdriver
import json

##Parse Options
parser = OptionParser()
parser.add_option("-g", "--group", dest="group", default="iati-technical",
                help="Google Group URL. Default is IATI-technical", metavar="TEXT")
parser.add_option("-j", "--json", dest="json", default="/vagrant/iati-technical.json",
                help="JSON output path. Default is /vagrant/iati-technical.json", metavar="PATH")
(options, args) = parser.parse_args()

def thread_to_dict(thread):
    parsed = {'name': thread.xpath('.//a')[0].text}
    parsed['url'] = thread.xpath('.//a')[0].attrib['href']
    raw_last_change = thread.xpath('.//span[@title]'
        )[0].attrib['title']
    parsed['last_change'] = raw_last_change
    info = thread.xpath('.//div[contains(@style,"right")]')[0]
    parsed['seen'] = int(info.xpath('.//span[@class]')[3].text.split()[0])
    parsed['posts'] = int(info.xpath('.//span[@class]')[2].text.split()[0])
    return parsed

GOOGLE_GROUP_BASE = 'https://groups.google.com/forum/'
GOOGLE_GROUP_URL = GOOGLE_GROUP_BASE + '#!forum/{}'
group_url = GOOGLE_GROUP_URL.format(options.group)

browser = webdriver.PhantomJS()
browser.set_window_size(1024, 7680)
browser.get(group_url)
time.sleep(5)
frontpage = fromstring(browser.page_source)
frontpage.make_links_absolute(GOOGLE_GROUP_BASE)
html_threads = frontpage.xpath('//div[@role="listitem"]')
threads = (thread_to_dict(thread) for thread in html_threads)

data = []

for thread in threads:
    print thread['name']
    browser.get(thread['url'])
    time.sleep(5)
    page = fromstring(browser.page_source)
    page.make_links_absolute(GOOGLE_GROUP_BASE)
    messages = page.xpath('//div[@class="LOFA24-nb-W"]')
    print "Posts: "+str(len(messages))
    print("")
    thread['post_data'] = []
    for i in range(0,len(messages)):
        obj = {}
        raw_msg = unicode(messages[i].text_content()).encode('utf-8')
        obj['author'] = raw_msg.strip().split("   ")[0]
        start = raw_msg.find("Other recipients:")+len("Other recipients:")
        end = raw_msg.rfind("Show trimmed content")
        obj['message'] =raw_msg[start:end].strip()
        thread['post_data'].append(obj)
    data.append(thread)
    
browser.quit()

print('Writing JSON...')
with open(options.json, 'w') as output_file:
    json.dump(data,output_file,ensure_ascii=False,indent=2)
print('Done.')
