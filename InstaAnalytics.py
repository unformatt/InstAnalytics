#!/usr/bin/python
# -*- coding: utf-8 -*-

import json, os, re, sys, requests
from bs4 import BeautifulSoup
from datetime import datetime


# List of users
users = [sys.argv[1]]



# ----------------------------------------
#  InstAnalytics function
# ----------------------------------------

def InstAnalytics():

    for user in users:

        # Load JSON
        with open('InstAnalytics.json') as ia_file:
            ia_data = json.load(ia_file)

        # Backup JSON
        with open('InstAnalytics_backup.json', 'w') as ia_file:
            json.dump(ia_data, ia_file, indent=4)

        page = requests.get('https://instagram.com/' + user)

        # Soup
        soup = BeautifulSoup(page.content, 'html.parser')
        js_str = re.match('.*?window\._sharedData =(.+?)<\/script.*?', unicode(soup.html), flags=re.I | re.M | re.S).groups()[0].strip(' ;')
        data = json.loads(js_str)

        # User's statistics
        user_data = data['entry_data']['ProfilePage'][0]['graphql']['user']
        posts = user_data['edge_owner_to_timeline_media']['count']
        followers = user_data['edge_followed_by']['count']
        following = user_data['edge_follow']['count']


        # Dictionary
        new_data = {
            'username': user,
            'date': datetime.now().strftime(timeFormat),
            'data': {
                'posts': posts,
                'followers': followers,
                'following': following
            }
        }

        # Add data to JSON
        ia_data.append(new_data)
        with open('InstAnalytics.json', 'w') as ia_file:
            json.dump(ia_data, ia_file, indent=4)

        print json.dumps(new_data)



# ----------------------------------------
#  Main
# ----------------------------------------

if __name__ == '__main__':
    timeFormat = "%Y-%m-%d"

    # Check if the JSON file exists, otherwise create it
    if not os.path.isfile('InstAnalytics.json'):
        ia_data = []
        with open('InstAnalytics.json', 'w') as ia_file:
            json.dump(ia_data, ia_file, indent=4)

    #try:
    print "InstAnalytics process started at: " + datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    InstAnalytics()
    print "InstAnalytics process finished at: " +  datetime.now().strftime("%d-%m-%Y %H:%M:%S")
