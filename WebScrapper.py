
# coding: utf-8

# In[71]:

import requests
from bs4 import BeautifulSoup
r = requests.get("http://pythonhow.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/")
c = r.content
soup = BeautifulSoup(c,"html.parser")
all = soup.find_all("div",{"class":"propertyRow"})
len(all)
page_nr = int(soup.find_all("a",{"class":"Page"})[-1].text)


# In[72]:

l = []
base_url = "http://pythonhow.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/t=0&s="
for page in range(0,page_nr*10,10):
    print(base_url+str(page)+".html")
    r = requests.get(base_url+str(page)+".html")
    c = r.content
    soup = BeautifulSoup(c,"html.parser")
    all = soup.find_all("div",{"class":"propertyRow"})
    for item in all:
        d={}
        d["Address"] = item.find_all("span",{"class":"propAddressCollapse"})[0].text
        try:
            d["Locality"] = item.find_all("span",{"class":"propAddressCollapse"})[1].text
        except:
            d["Locality"] = None
        d["Price"] = item.find_all("h4",{"class":"propPrice"})[0].text.replace('\n',"").replace(" ","")
        try:
           d["Beds"] = item.find("span",{"class":"infoBed"}).find("b").text
        except:
            d["Beds"] = None
        try:
            d["Area"] = item.find("span",{"class":"infoSqFt"}).find("b").text
        except:
            d["Area"] = None
        try:
            d["Full Bath"] = item.find("span",{"class":"infoValueFullBath"}).find("b").text
        except:
            d["Full Bath"] = None
        try:
            d["Half Bath"] = item.find("span",{"class":"infoValueHalfBath"}).find("b").text
        except:
            d["Half Bath"] = None
        for column_group in item.find_all("div",{"class":"columnGroup"}):

            for feature_group,feature_name in zip(column_group.find_all("span",{"class":"featureGroup"}) , column_group.find_all("span",{"class":"featureName"})):

                if("Lot Size" in feature_group.text):
                    d["Lot Size"] = feature_name.text
        l.append(d)


# In[73]:

print(len(l))
import pandas
df = pandas.DataFrame(l)


# In[74]:

df


# In[75]:

df.to_csv("Output.csv")


# In[ ]:



