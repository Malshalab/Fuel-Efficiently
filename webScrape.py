import requests
from geopy import distance
from geopy.geocoders import Nominatim
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import *

geocoder=Nominatim(user_agent="I Know python")


url="http://www.ontariogasprices.com/GasPriceSearch.aspx?typ=adv&fuel=A&srch=0&area=Milton&site=Ontario&station=All%20Stations&tme_limit=4"
page= requests.get(url)
c=page.content
soup=BeautifulSoup(c, 'html.parser')

lists = soup.find_all('div', id="pp_table")

for my_list in lists:
    dl=my_list.find_all("dl",{"class":"address"})
    div=my_list.find_all('div', class_="price_num")
    a=my_list.find_all('a',class_="p_area")


locationlist=[]
pricelist=[]
areaList=[]

for wrapper in dl:
    location=(wrapper.text)
    locationlist.append(location)
    location_list=[s.replace("\n"," ") for s in locationlist]
    location_list = [x.strip(' ') for x in location_list]


for wrapper2 in div:
   price=(wrapper2.text)
   pricelist.append(price)


for wrapper3 in a:
   area=(wrapper3.text)
   areaList.append(area)


real_location=[]
z=0
x=[]
new_list=[]


for x in location_list:
  count=0
  for element in x:
      if(element.isdigit()):
          break;
      count+=1
  x=x[count:len(x)]
  new_list.append(x)
#print(new_list)
exitCondition1="&"
exitConditionTwo="near"

final_list=[]

exitCondition1="&"
exitConditionTwo="near"

final_list=[]

for condition in new_list:
    if exitCondition1 in condition:
        condition = condition[0:condition.index(exitCondition1)]
    elif exitConditionTwo in condition:
        condition = condition[0:condition.index(exitConditionTwo)]
    final_list.append(condition)





distances=[]


for destination in final_list:
    coordinates1=geocoder.geocode(destination)
    lat1,long1=(coordinates1.latitude),(coordinates1.longitude)
    place1=(lat1,long1)


    home="147 farrington crossing"
    coordinatesHome=geocoder.geocode(home)
    lat2,long2=(coordinatesHome.latitude),(coordinatesHome.longitude)
    place2=(lat2,long2)
    distanceOne=distance.distance(place2,place1).km
    distances.append(distanceOne)



#Best Gas Station Algorithm
def calculateWeight(distance, gasPrice, carConsumption, fuelTankSize):
    gasExpended=distance*carConsumption
    moneySpent=(gasExpended*gasPrice)+(gasPrice*fuelTankSize)
    return moneySpent

#Sorting Algorithm Of Choice
def insertion_sort(array):
    for i in range(1, len(array)):
        key_item = array[i]
        j = i - 1
        while j >= 0 and array[j] > key_item:
            array[j + 1] = array[j]
            j -= 1
        array[j + 1] = key_item


weights = []
prices=[]

for iteratioj in pricelist:
    prices.append(float(iteratioj))


final_location=[]

for i in range(len(final_list)):
    final_price=prices[i]
    final_distance=distances[i]
    final_location.append(final_list[i])
    final_info=calculateWeight(final_distance,final_price,8.9,70)
    final_info=final_info/100
    weights.append(final_info)



#Sorting Algorithm Of Choice
def insertion_sort(final_location, array):
    for i in range(1, len(array)):
        key_item1 = array[i]
        key_item2 = final_location[i]
        j = i - 1
        while j >= 0 and array[j] > key_item1:
            array[j + 1] = array[j]
            final_location[j+1] = final_location[j]
            j -= 1
        array[j + 1] = key_item1
        final_location[j+1] = key_item2

insertion_sort(final_location,weights)
final_dict = {}

for i in range(len(weights)):
  if(weights[i] not in final_dict.keys()):
    final_dict[weights[i]] = final_location[i]



cheapest_price=next(iter(final_dict))


def printInput():
    lbl.config(text="Cheapest Gas location is: " + str(final_location[0])+" cheapest Gas Price is: "+str(cheapest_price))

#creating the window
root=tk.Tk()

canvas=tk.Canvas(root, height=700, width=700, bg="#263D42")
canvas.pack()

frame=tk.Frame(root,bg="white")
frame.place(relwidth=0.8,relheight=0.8, relx=0.1, rely=0.1)


#create the button
calculateButton = Button(text="Calculate Cheapest",command=lambda:printInput())
calculateButton.place(relx=0.5, rely=0.5, anchor=CENTER)



#display box
lbl = tk.Label(frame, text = "")
lbl.pack()



#running the app
mainloop()
root.mainloop()
