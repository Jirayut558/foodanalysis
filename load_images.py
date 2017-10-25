# coding: utf-8

# Searching and Downloading Google Images/Image Links

# Import Libraries

# coding: UTF-8
import csv
import time  # Importing the time library to check the time of code execution
import sys  # Importing the System Library
import os
from urllib2 import Request, urlopen
from urllib2 import URLError, HTTPError

########### Edit From Here ###########

# This list is used to search keywords. You can edit this list to search for google images of your choice. You can simply add and remove elements of the list.
search_keyword = ['Australia']

# This list is used to further add suffix to your search term. Each element of the list will help you download 100 images. First element is blank which denotes that no suffix is added to the search keyword of the above list. You can edit the list by adding/deleting elements from it.So if the first element of the search_keyword is 'Australia' and the second element of keywords is 'high resolution', then it will search for 'Australia High Resolution'
keywords = [' high resolution']


########### End of Editing ###########


def loadLinks():
    foods = []
    with open('links.csv') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            # print(row)
            # item = []
            food = { 'type': row[0], 'link': row[1] }
            foods.append(food)
    return foods

# Downloading entire Web Document (Raw Page Content)
def download_page(url):
    version = (3, 0)
    cur_version = sys.version_info
    if cur_version >= version:  # If the Current Version of Python is 3.0 or above
        import urllib.request  # urllib library for Extracting web pages
        try:
            headers = {}
            headers[
                'User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
            req = urllib.request.Request(url, headers=headers)
            resp = urllib.request.urlopen(req)
            respData = str(resp.read())
            return respData
        except Exception as e:
            print(str(e))
    else:  # If the Current Version of Python is 2.x
        import urllib2
        try:
            headers = {}
            headers[
                'User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
            req = urllib2.Request(url, headers=headers)
            response = urllib2.urlopen(req)
            page = response.read()
            return page
        except:
            return "Page Not found"


# Finding 'Next Image' from the given raw page
def _images_get_next_item(s):
    start_line = s.find('rg_di')
    if start_line == -1:  # If no links are found then give an error!
        end_quote = 0
        link = "no_links"
        return link, end_quote
    else:
        start_line = s.find('"class="rg_meta"')
        start_content = s.find('"ou"', start_line + 1)
        end_content = s.find(',"ow"', start_content + 1)
        content_raw = str(s[start_content + 6:end_content - 1])
        return content_raw, end_content


# Getting all links with the help of '_images_get_next_image'
def _images_get_all_items(page):
    items = []
    while True:
        item, end_content = _images_get_next_item(page)
        if item == "no_links":
            break
        else:
            items.append(item)  # Append all the links in the list named 'Links'
            time.sleep(0.1)  # Timer could be used to slow down the request for image downloads
            page = page[end_content:]
    return items

foods = loadLinks()
for food in foods:
    print(food['link'])
############### Main ###################
    photopath = "Photos/" + food['type'] + '/'
    print(photopath)
    if not os.path.exists(photopath):
        os.makedirs(photopath)
    url = food['link']
    raw_html = (download_page(url))
    items = _images_get_all_items(raw_html)

    print(items)

    k=0
    while k<len(items):
        try:
            req = Request(items[k], headers={"User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"})
            response = urlopen(req, None, 15)
            output_file = open( photopath + str(k + 1) + ".jpg", 'wb')

            data = response.read()
            output_file.write(data)
            response.close();
            k+=1
        except Exception as e:
            k+=1
            print(e)

# ############## Main Program ############
