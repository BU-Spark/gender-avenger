# Filename: sxsw.py
# Author: Dharmesh Tarapore <dharmesh@cs.bu.edu>
# Description: SXSW Speaker directory scraper.

import pandas as pd 
from bs4 import BeautifulSoup
import gender_guesser.detector as gdetector

d = gdetector.Detector()

speakers = pd.DataFrame()

# Set this to wherever you save the CES Speaker directory HTML page: 
# https://www.ces.tech/Conference/Speaker-Directory.aspx
fp = "/Users/dharmesh/sxswspkdir.htm"
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
#companies = []
genders = []

phtml = BeautifulSoup(file, features='lxml')
m = phtml.findAll('div', attrs={'class': 'sm-col sm-col-6 md-col-4 p2'})

for speaker in m:
	name = speaker.find('p', attrs={'class': 'h3 bold uppercase center m0'})
	if name != None:
		name = name.text
		name = " ".join(name.split())
		name = name.split(" ")
		if len(name) > 1:
			first_names.append(name[0])
			last_names.append(name[1])
			gguess = d.get_gender(name[0])
			if gguess == "unknown":
				gguess = d.get_gender(name[1])
			genders.append(gguess)
			title = speaker.find('p', attrs={'class': 'h5 center m0'})
			if title != None:
				title = title.text
				title = " ".join(title.split())
				titles.append(title)
			else:
				titles.append("Not found")
		else:
			continue
	else:
		continue


# Put this all in a Pandas DataFrame
speakers['first_name'] = first_names
speakers['last_name'] = last_names
speakers['title'] = titles
speakers['gender'] = genders

speakers.to_excel("../output/sxsw2019.xlsx")

