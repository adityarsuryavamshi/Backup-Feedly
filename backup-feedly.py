#!/usr/bin/python3

import requests
import os
import json
import time
import argparse

SILENT=True
 

def get_opml(access_token): 
    headers = {"Authorization" : "OAuth " + access_token}
    
    if not SILENT:
        print("Fetching OPML file...")
    
    r = requests.get("https://cloud.feedly.com/v3/opml", headers = headers)
    
    if r.status_code == 200:
        filename = "feedly-backup-" + str(int(time.time())) + ".opml"
        with open(filename, "w") as f:
            f.write(r.text)
    
        if not SILENT:
            print("Saved Subscription feeds to file: ", filename)
    
    else:
        print("Error while fetching OPML file, status code: " + str(r.status_code))
        print(r.json())



def get_saved_items(user_id, access_token): 
    headers = {"Authorization" : "OAuth " + access_token}
    url = "https://cloud.feedly.com/v3/streams/contents?streamId=user/" + user_id + "/tag/global.saved&count=10000"    
    
    if not SILENT:
        print("Fetching saved items...")
    
    r = requests.get(url, headers = headers)
    
    if r.status_code == 200:
        response = r.json()
        items = response["items"]
        url_list = []
        count = 1
    
        for i in items:
            content_title = i["title"]
            try:
                content_url = i["canonical"][0]["href"]
            except KeyError:
                content_url = i["alternate"][0]["href"]
            url_list.append((content_title, content_url))
        
            if not SILENT:
                print()
                print("[" +  str(count) + "]" + " Title : ", content_title)
                print("[" +  str(count) + "]" + " URL: ", content_url)
                count += 1
        
        return url_list
    
    else:
        print("Error while fetching saved items, status code: " + str(r.status_code))
        print(r.json())
        exit(1)



def make_bookmark(url_list):
    html = """<!DOCTYPE NETSCAPE-Bookmark-file-1>
<!--This is an automatically generated file.
    It will be read and overwritten.
    Do Not Edit! -->
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<Title>Bookmarks</Title>
<H1>Bookmarks</H1>
<DL><p>
"""
    
    for i in url_list:
        item = '    <DT><A HREF="' + i[1] + '">' + i[0] + '</a>\n'
        html += item
    html += '</DL><p>\n'
    filename = "feedly-saved-" + str(int(time.time())) + ".html"
    
    with open(filename, "w") as f:
        f.write(html)
    
    if not SILENT:
        print()
        print("Saved contents to Bookmark file: " + str(filename))
        print()



def main(fetch_saved, fetch_opml): 
    try:
        user_id = os.environ['FEEDLY_USER_ID']
        access_token = os.environ['FEEDLY_ACCESS_TOKEN']
    except KeyError:
        print("Please Set the Environment Variables FEEDLY_USER_ID, FEEDLY_ACCESS_TOKEN")
        exit(1)
    
    if fetch_saved:
        url_list = get_saved_items(user_id, access_token)
        make_bookmark(url_list)
    
    if fetch_opml:
        get_opml(access_token)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A Command Line Utility to backup saved items (Read Later's) and subscriptions from feedly")

    parser.add_argument("-v", "--verbose", action='store_true',  default=False, help="Print what is being done")
    parser.add_argument("--no-saved", action='store_true', default=False, help="Don't fetch and make a bookmark file of saved items")
    parser.add_argument("--no-opml", action='store_true', default=False, help="Don't download OPML file containing the subscribed feeds")

    args = parser.parse_args()
    
    SILENT= not args.verbose
    fetch_saved = not args.no_saved
    fetch_opml = not args.no_opml

    main(fetch_saved, fetch_opml)
