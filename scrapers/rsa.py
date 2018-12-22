# Filename: rsa.py
# Author: Dharmesh Tarapore <dharmesh@cs.bu.edu>
# Description: Scrapes RSA conference site to analyze gender disparity.
#              

import pandas as pd 
from bs4 import BeautifulSoup
import gender_guesser.detector as gdetector

d = gdetector.Detector()

speakers = pd.DataFrame()

# Set this to wherever you save the RSA Speaker directory HTML page: 
# https://www.rsaconference.com/events/us19/speakers?showEnrolled=false
fp = "/Users/dharmesh/rsaspkdir.htm"
file = open(fp, "r")
file = file.read()

'''
    1. Find first and last name.
    2. Put through classifier to get gender.
    3. Store organization
    4. Store title
    5. Put in CSV
'''

first_names = []
last_names = []
titles = []
companies = []
genders = []

phtml = BeautifulSoup(file, features='lxml')
m = phtml.findAll('div', attrs={'class': 'rfComp-speaker-results'})
m = m[0]
m = m.findAll('div', attrs={'class': 'list-group-item'})
m = m[1:]

for speaker in m:
	name = speaker.find('div', attrs={'class': 'rf-list-item-one'})
	if name != None:
		name = name.text
		name = " ".join(name.split())
		name = name.split(" ")
		first_names.append(name[0])
		last_names.append(name[1])
		gguess = d.get_gender(name[0])
		if gguess == "unknown":
			gguess = d.get_gender(name[1])
		genders.append(gguess)
	else:
		first_names.append("Not found")
		last_names.append("Not found")
		genders.append("Not found")
	company = speaker.find('div', attrs={'class': 'rf-list-item-three'})
	title = speaker.find('div', attrs={'class': 'rf-list-item-two'})
	if company != None:
		company = company.text
		companies.append(company)
	if title != None:
		titles.append(title.text)


# Put this all in a Pandas DataFrame
speakers['first_name'] = first_names
speakers['last_name'] = last_names
speakers['title'] = titles
speakers['organization'] = companies
speakers['gender'] = genders

speakers.to_excel("../output/rsa2019.xlsx")
