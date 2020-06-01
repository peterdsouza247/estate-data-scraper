import requests, re, pandas
from bs4 import BeautifulSoup

req = requests.get("http://www.pyclass.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/", headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
body = req.content
soup = BeautifulSoup(body, "html.parser")
page_nr = soup.find_all("a", {"class":"Page"})[-1].text

data_entries = []

base_url = "http://www.pyclass.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/t=0&s="
for page in range(0, int(page_nr) * 10, 10):
    request = requests.get(base_url + str(page) + ".html", headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
    body_content = request.content
    soup = BeautifulSoup(body_content, "html.parser")
    all = soup.find_all("div", {"class":"propertyRow"})
    for item in all:
        dict = {}
        dict["Address"] = item.find_all("span", {"class","propAddressCollapse"})[0].text
        
        try:
            dict["Locality"] = item.find_all("span",{"class", "propAddressCollapse"})[1].text
        except:
            dict["Locality"] = None
        
        dict["Price"] = item.find("h4",{"class", "propPrice"}).text.replace("\n", "").replace(" ", "")
        
        try:
            dict["Beds"] = item.find("span", {"class", "infoBed"}).find("b").text
        except:
            dict["Beds"] = None
    
        try:
            dict["Area"] = item.find("span", {"class", "infoSqFt"}).find("b").text
        except:
            dict["Area"] = None
    
        try:
            dict["Full Baths"] = item.find("span", {"class", "infoValueFullBath"}).find("b").text
        except:
            dict["Full Baths"] = None

        try:
            dict["Half Baths"] = item.find("span", {"class", "infoValueHalfBath"}).find("b").text
        except:
            dict["Half Baths"] = None
        
        for column_group in item.find_all("div", {"class":"columnGroup"}):
            for feature_group, feature_name in zip(column_group.find_all("span", {"class":"featureGroup"}), column_group.find_all("span", {"class":"featureName"})):
                if "Lot Size" in feature_group.text:
                    dict["Lot Size"] = feature_name.text
        data_entries.append(dict)

df = pandas.DataFrame(data_entries)
df.to_csv("estate-data.csv")