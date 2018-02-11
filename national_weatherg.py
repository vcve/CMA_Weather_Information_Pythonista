#-*- coding: utf-8 -*-
import time
import location
import urllib.request
from bs4 import BeautifulSoup 
import re
import clipboard

location.start_updates()
time.sleep(3)
loc = location.get_location()
location.stop_updates()  # stop GPS hardware ASAP to save battery
location.stop_updates()
lat = format(loc['latitude'])
lon = format(loc['longitude'])

url = 'http://m.weather.com.cn/d/town/index?lat=' + lat + '&lon=' + lon
#print(url)
#content=requests.get(url).content
#content = content.decode('utf-8')

content = urllib.request.urlopen(url)
soup = BeautifulSoup(content, "html5lib")
# -------Location&Generally -------------
loca_info = ((soup.select('[class="wrap"]') + soup.select('[class="n_wd"]')  + soup.select('[class="zwx"]')))
localist=[]
for loca in loca_info:
	localist.append(BeautifulSoup.get_text(loca))
#print(localist)

locali=[]
for lo in localist:
	locali.append(re.sub('\s+', ',', lo))
add_gens=(''.join(list(locali[0])))
add_gen=(add_gens.split(','))

a=''
add = add_gen[1:4]
updatetime = add_gen[5][0:5]
add = a.join(add)

wea_gens=(''.join(list(locali[1])))
wea_gen =(wea_gens.split(','))
wet = wea_gen[5:7]
wet = a.join(wet)
wea ='直至'+updatetime + '，天气'+ wea_gen[2]+'，'+'气温为' + wea_gen[1]+'度，'+wea_gen[3]+wea_gen[4]+'，'+ wet

# -------------hourly -------------
times = soup.select('[class="timeLi"]')
temps = soup.select('[class="tempLi"]')
timelist = []
templist = []
for t in times:
	timelist.append(t.get_text())
for temp in temps:
	templist.append(temp.get_text())
timedic = dict(zip(timelist, templist))
#-----------day_info-----------
daytime=soup.select('[class="dayTime"]') 
day_icon=soup.select('[class="day_icon"]')
day_fl=soup.select('[class="wefther-fl"]')
daytimelist = []
day_iconlist=[]
for day in daytime:
	daytimelist.append(day.get_text())
for icon in day_icon:
	day_iconlist.append(icon.get_text())

fllist=[]
for fl in day_fl:
	fllist.append(BeautifulSoup.get_text(fl))
flist=[]
for f in fllist:
	flist.append(f.strip(' \t\n\r'))

daydic = dict(zip(daytimelist,day_iconlist))
dayfldic= dict(zip(daytimelist,flist))
#print(daydic)
#print(dayfldic)
#-----------others-----------
#others = soup.select('[class="shzs"]') + soup.select('[class="uv"]') + soup.select('[class="xc"]') + soup.select('[class="cy"]') + soup.select('[class="gm"]') + soup.select('[class="yd"]') + soup.select('[class="ly"]') + soup.select('[class="ls"]') + soup.select('[class="kqwr"]')
#otherlist=[]
#for oth in others:
	#otherlist.append(BeautifulSoup.get_text(oth))
#otherli=[]
#for o in otherlist:
	#otherli.append(re.sub('\s+', ',', o))
#print(otherli)
#-----------others2-----------
url = ('http://m.weather.com.cn/d/town/idetail?lat='+ lat +'&lon='+ lon + '&i=ct')
content = urllib.request.urlopen(url)
soup = BeautifulSoup(content, "html5lib")
#print(soup)
chuanyilist=[]
chuanyi=soup.find(id="swiper-container1")
for string in chuanyi.stripped_strings:
	chuanyilist.append(string)
#print(chuanyilist)
cylist=[]
for cy in chuanyilist:
	cylist.append(cy.replace('\t',''))
clist=[]
for cy in cylist:
	clist.append(cy.replace('\n',''))
cli=[]
for cy in clist:
	cli.append(''.join(cy.split()))
#-----------------
day0=cli[0:5]
day1=cli[5:10]
day2=cli[10:15]
day3=cli[15:20]
day4=cli[20:25]
day5=cli[25:30]
day6=cli[30:35]
chuanlist=[day0,day1,day2,day3,day4,day5,day6]

#-----------------
riqilist=[]
riqi=soup.find(id="contrast")
for string in riqi.stripped_strings:
	riqilist.append(string)
chuan=dict(zip(riqilist,chuanlist))
#print(chuan)
#-----------------
chuantoday=str('，'.join(chuan['今天']))

output=(add)+'， '+(wea)+('。今天全天: ')+(chuantoday)
#print(output)
new_clip = output
clipboard.set(new_clip)
print(new_clip)
import webbrowser
webbrowser.open('workflow://')
