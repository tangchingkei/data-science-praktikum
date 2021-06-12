# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 14:56:45 2021

@author: JonathanW
"""

import os
import pandas as pd

#change to directory where the files are stored
os.chdir("C:/Users/JonathanW/Projects/Spyder/PraktikumDataScience/Rona_Data")


#import data from csv
testing = pd.read_csv("covid-19-testing-policy.csv")
vaccination = pd.read_csv("covid-vaccination-policy.csv")
face_cover = pd.read_csv("face-covering-policies-covid.csv")
events = pd.read_csv("public-events-covid.csv")
transport = pd.read_csv("public-transport-covid.csv")
school_closures = pd.read_csv("school-closures-covid.csv")
stay_home = pd.read_csv("stay-at-home-covid.csv")

owid = pd.read_csv("owid-covid-data.csv")


#Series with g20 members according to wikipedia + spain
g20_members = pd.Series(["Argentina", "Australia", "Brazil", "Canada", "China", "France", "Germany", "India", "Indonesia", "Italy", "Japan", "South Korea", "Mexico", "Russia", "Saudi Arabia", "South Africa", "Turkey", "United Kingdom", "United States", "Spain", "European Union"])

#filter data array for locations that match g20 countries
g20_data = owid[owid["location"].isin(g20_members)].reset_index(drop=True)