import requests
import json


url='http://api.openweathermap.org/data/2.5/forecast?q=Colorado Springs&units=imperial&appid=811c578a53b40361b336ae061ff39aba'
r=requests.get(url)
results=r.json()
temp_list=[i["main"]["temp"] for i in results["list"]]
uniform_l=["S/S shirt and shorts","L/S shirt and shorts","L/S shirt,jacket and shorts","L/S shirt,jacket,pants,hat and gloves"]
def uniform():
    if int(temp_list[0])>60:
        uniform="S/S shirt and shorts"
    elif int(temp_list[0]) in range(50,60):
        uniform="L/S shirt and shorts"
    elif int(temp_list[0]) in range(40,50):
        uniform="L/S shirt,jacket and shorts"
    else:
        uniform="L/S shirt,jacket,pants,hat and gloves"
    return uniform
print(uniform())