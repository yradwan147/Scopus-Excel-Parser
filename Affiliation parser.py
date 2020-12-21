import pandas as pd
import os
import numpy
import csv
import pycountry
import re
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def close_overlay():
		time.sleep(3)
		try:
			close_overlay = driver.find_element_by_class_name("_pendo-close-guide")
		except:
			close_overlay = driver.find_element_by_class_name("_pendo-close-guide_")
		close_overlay.click()

countries = []
for i in list(pycountry.countries):
    countries.append(i.name)
centers = ["Smart", "Nanoelectronics", "School", "Nisc", "Wireless", "Mechanical", "Bioinformatics", "Management", "Graduate"]

PATH = os.path.dirname(os.path.realpath(__file__))

df = pd.read_csv(PATH + '/differences.csv',) #you could add index_col=0 if there's an index
author_affil_int =[]
names_int = []
ids_int = []
author_affil_int.append(df['Authors with affiliations'])
names_int.append(df["Title"])
ids_int.append(df["Author(s) ID"])

data_author = author_affil_int[0].to_numpy()
data_name = names_int[0].to_numpy()
data_ids = ids_int[0].to_numpy()
driver = webdriver.Firefox(executable_path=PATH + r'\geckodriver.exe')
driver.get("https://08105aj8u-1103-y-https-www-scopus-com.mplbci.ekb.eg/authid/detail.uri?authorId=7103379659")
myElem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, '_58_login')))
login = driver.find_element_by_id("_58_login")
login.send_keys("yradwan147.yr@gmail.com")
login2 = driver.find_element_by_id("_58_password")
login2.send_keys("TE_Data1")
login_button = driver.find_element_by_css_selector("button.btn.btn-default.mb-2.btn-primary")
login_button.click()

with open(PATH + "\Output.csv", "w+") as output:
                writer = csv.writer(output)
                writer.writerow(["Title", "Affiliated Author", "Affiliation", "Scopus ID", "Scopus Profile Link", "Scopus Name", "Scopus Titles"])

counter = 0
for x in data_author:
    counter1 = 0
    names = []
    affiliations = []
    ids = []
    scopus_names = []
    scopus_titles = []
    try:
        authors = x.split(";")
    except:
        print(x)
    for author in authors:
        name = ""
        if "Nile University" in author:
            idIndex = authors.index(author)
            idFinal = (data_ids[counter].split(';'))[idIndex]
            ids.append(idFinal)
            driver.get("https://08105aj8u-1103-y-https-www-scopus-com.mplbci.ekb.eg/authid/detail.uri?authorId=" + str(idFinal))
            time.sleep(1)
            try:
                button = driver.find_element_by_id("scopus-author-profile-page-control-microui__scopus-author-general-information__showAllAuthorInfo")
                try:
                    button.click()
                except:
                    close_overlay()
                    button.click()
                flag = True
                time.sleep(1)
            except:
                flag = False
            
            try:
                scopus_names.append(driver.find_elements_by_class_name("author-general-details-title")[0].text)
                if (flag):
                    scopus_titles.append(driver.find_element_by_id("scopus-author-profile-page-control-microui__scopus-author-general-information__showAllInfoNameVariants").text)
                else:
                    scopus_titles.append(" ")
            except:
                scopus_names.append(" ")
                scopus_titles.append(" ")
            counter1 += 1
            name_split = author.split(",")[:2]
            for i in name_split:
                name += i
            name += " "
            ##print(name)
            names.append(name)
            affs = author.split("Egypt")
            for aff in affs:
                if "Nile University" in aff:
                    for i in countries:
                        if i in aff:
                            aff = aff[(aff.find(i) + len(i) + 2):]
                    if name.replace(" ", ", ") in aff:
                        aff = aff[(aff.find(name.replace(" ", ", ")) + len(name.replace(" ", ", "))):]
                    elif (name[1:].replace(" ", ", ")) in aff:
                        aff = aff[(aff.find(" " + name[1:].replace(" ", ", ")) + len(" " + name[1:].replace(" ", ", "))):]
                    if "," in aff[:3]:
                        aff = aff[aff.find(",") + 1:]
                        aff.strip()
                    # for x in centers:
                    #     if x in aff:
                    #         aff = aff[(aff.find(x)):]
                    affiliations.append(aff.strip())
    with open(PATH + "\Output.csv", "a", encoding="utf-8") as output:
                writer = csv.writer(output)
                list_output = []
                ##print(str(data_name[counter]) + str(counter))
                for i in range(counter1):
                    url = "https://www.scopus.com/authid/detail.uri?origin=resultslist&authorId=" + str(ids[i]) + "&zone="
                    writer.writerow([data_name[counter], names[i], affiliations[i], ids[i], url, scopus_names[i], scopus_titles[i]])
                #for j in range(counter1):
                #    writer.writerow(list_output)
    counter += 1