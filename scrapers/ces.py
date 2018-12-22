# Filename: ces.py
# Author: Dharmesh Tarapore <dharmesh@cs.bu.edu>
# Description: Analyzes saved Speaker directory HTML page.

import pandas as pd 
from bs4 import BeautifulSoup
import gender_guesser.detector as gdetector

d = gdetector.Detector()

speakers = pd.DataFrame()

# Set this to wherever you save the CES Speaker directory HTML page: 
# https://www.ces.tech/Conference/Speaker-Directory.aspx
fp = "/Users/dharmesh/cesspkdir.htm"
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
m = phtml.findAll('aside', attrs={'class': 'speaker-photo directory small'})

for speaker in m:
	name = speaker.find('h3', attrs={'class': 'speaker-name'})

	if name != None:
		name = name.text
		name = " ".join(name.split())
		name = name.split(" ")
		if name[0] == "Dr.":
			first_names.append(name[1])
			last_names.append(name[2])
		else:
			first_names.append(name[0])
			last_names.append(name[1])
		# Guess gender
		gguess = d.get_gender(name[0])
		if gguess == "unknown":
			gguess = d.get_gender(name[1])
		genders.append(gguess)
	else:
		first_names.append("Not found")
		last_names.append("Not found")
		genders.append("Not found")

	company = speaker.find('h4', attrs={'class': 'speaker-company'})
	title = speaker.find('h4', attrs={'class': 'speaker-title'})

	if company != None:
		companies.append(company.text)
	else:
		companies.append("Not found")

	if title != None:
		titles.append(title.text)
	else:
		titles.append("Not found")

# Put this all in a Pandas DataFrame
speakers['first_name'] = first_names
speakers['last_name'] = last_names
speakers['title'] = titles
speakers['organization'] = companies
speakers['gender'] = genders

speakers.to_excel("../output/ces2019.xlsx")

