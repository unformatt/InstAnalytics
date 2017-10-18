#!/usr/bin/python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from datetime import datetime
import json, time, os, re



# List of users
users = ['yotta_life']



# ----------------------------------------
#  InstAnalytics function
# ----------------------------------------

def InstAnalytics():

	# Launch browser
	browser = webdriver.PhantomJS(desired_capabilities=dcap)

	for user in users:

		# Load JSON
		with open('InstAnalytics.json') as iaFile:
			iaDictionary = json.load(iaFile)

		# Backup JSON
		with open('InstAnalytics_backup.json', 'w') as iaFile:
			json.dump(iaDictionary, iaFile, indent=4)

		# User's profile
		browser.get('https://instagram.com/' + user)
		time.sleep(0.5)

		# Soup
		soup = BeautifulSoup(browser.page_source, 'html.parser')

		# User's statistics
		postsT     = soup.html.body.span.section.main.article.findAll('ul',recursive=False)[0].findAll('li')[0].findAll('span')[1].getText()
		followersT = soup.html.body.span.section.main.article.findAll('ul',recursive=False)[0].findAll('li')[1].findAll('span')[1].getText()
		followingT = soup.html.body.span.section.main.article.findAll('ul',recursive=False)[0].findAll('li')[2].findAll('span')[1].getText()

		# Remove all non-numeric characters
		posts     = int(re.sub('[^0-9]', '', postsT))
		followers = int(re.sub('[^0-9]', '', followersT))
		following = int(re.sub('[^0-9]', '', followingT))

		# Convert k to thousands and m to millions
		if 'k' in postsT: 	  posts     = posts     * 1000
		if 'k' in followersT: followers = followers * 1000
		if 'k' in followingT: following = following * 1000
		if 'm' in postsT: 	  posts     = posts     * 1000000
		if 'm' in followersT: followers = followers * 1000000
		if 'm' in followingT: following = following * 1000000

		# Dictionary
		userDic = {
			'username': user,
			'date': datetime.now().strftime(timeFormat),
			'data': {
				'posts': posts,
				'followers': followers,
				'following': following
			}
		}

		# Add data to JSON
		iaDictionary.append(userDic)
		with open('InstAnalytics.json', 'w') as iaFile:
			json.dump(iaDictionary, iaFile, indent=4)

		print '|', user

	# Quit browser
	browser.quit()

	# Remove ghostdriver.log
	if os.path.isfile('ghostdriver.log') == True:
		os.remove('ghostdriver.log')



# ----------------------------------------
#  Main
# ----------------------------------------

if __name__ == '__main__':

	# Desired capabilities for PhantomJS
	dcap = dict(DesiredCapabilities.PHANTOMJS)
	dcap['phantomjs.page.settings.userAgent'] = 'Googlebot/2.1 (+http://www.googlebot.com/bot.html)'

	timeFormat = "%Y-%m-%d"

	# Check if the JSON file exists, otherwise create it
	if os.path.isfile('InstAnalytics.json') == False:
		iaDictionary = []
		with open('InstAnalytics.json', 'w') as iaFile:
			json.dump(iaDictionary, iaFile, indent=4)

	try:
		print "InstAnalytics process started at: " + datetime.now().strftime("%d-%m-%Y %H:%M:%S")
		InstAnalytics()
		print "InstAnalytics process finished at: " +  datetime.now().strftime("%d-%m-%Y %H:%M:%S")
	except Exception, e:
		print 'Error', e	
	

