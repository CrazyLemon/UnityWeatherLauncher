#!/usr/bin/env python
# coding=utf-8
#
# The point of this script is to provide an easy access to
# current weather/forecast. Just one click on the launcher icon and
# write the city you'd like to see current weather and forecast for the next
# N days.

# Import
import commands, locale, urllib, json, subprocess, os, requests, shutil, pynotify
import datetime

# Variables
entryTextSl = "Vnesite mesto"
entryTextEn = "Enter city"
textSl = "Vremenska napoved za:"
textEn = "Weather forecast for:"
locationSl = "Kraj"
locationEn = "Location"
weatherKey = "insert_your_api_key_here"

# Localization part
locale.setlocale(locale.LC_ALL, '')
locString = locale.getlocale()[0].split('_')[0]

if locString == 'sl':
    entryText = entryTextSl
    text = textSl
    location = locationSl
else:
    entryText = entryTextEn
    text = entryTextEn
    location = locationEn

# Shell part
cityOutput = subprocess.Popen('zenity --entry --entry-text="{}" --text="{}:" --width=250 --height=150'.format(entryText,text), shell=True, stdout = subprocess.PIPE)
city = cityOutput.stdout.read().rstrip('\n').title()

# OpenWeather
weatherUrl = ("http://api.openweathermap.org/data/2.5/weather?q=%s&units=metric&appid=%s") % (city, weatherKey)
#forecastUrl = ("http://api.openweathermap.org/data/2.5/forecast/daily?q=%s&units=metric&cnt=3&appid=%s") % (city, weatherKey)

# Get weather data - current weather
weatherData = urllib.urlopen(weatherUrl)
weatherJson = json.loads(weatherData.read())

temp = weatherJson["main"]["temp"]
wind = weatherJson["wind"]["speed"] * 3.6
pressure = weatherJson["main"]["pressure"]
humidity = weatherJson["main"]["humidity"]
time = datetime.datetime.fromtimestamp(int(weatherJson["dt"])).strftime("%H:%M")
sunset = datetime.datetime.fromtimestamp(int(weatherJson["sys"]["sunset"])).strftime("%H:%M")
sunrise = datetime.datetime.fromtimestamp(int(weatherJson["sys"]["sunrise"])).strftime("%H:%M")

icon = weatherJson["weather"][0]["icon"]
iconUrl = "http://openweathermap.org/img/w/{}.png".format(icon)
iconPath = "{}/{}.png".format(os.getcwd(),icon)

# Handle saving weather icons
if not os.path.isfile(iconPath):
    r = requests.get(iconUrl, stream=True)
    with open('{}.png'.format(icon), 'wb') as out_file:
        shutil.copyfileobj(r.raw, out_file)
    del r

# Show notification for current weather
msg = '{}°C   {}km/h   {}hPa   {}%\nVzhod: {}   Zahod: {}'.format(temp,wind,pressure,humidity,sunrise,sunset)

n = pynotify.Notification('{}   -   {}'.format(city,time),msg,iconPath)
n.set_timeout(50)

if not pynotify.init("Notification test"):
	sys.exit(1)
if not n.show():
    print("Something went wrong")
    sys.exit(1)

#forecast
#forecastData = urllib.urlopen(forecastUrl)
#forecastJson = json.loads(forecastData.read())

# Forecast variables
#
# tomorrow
# tomorrow = datetime.datetime.fromtimestamp(int(forecastJson["list"][1]["dt"])).strftime("%H:%M:%S %d.%m.%Y")
# tomorrowTempMorn = forecastJson["list"][1]["temp"]["morn]
# tomorrowTempDay = forecastJson["list"][1]["temp"]["day"]
# tomorrowTempNight = forecastJson["list"][1]["temp"]["night"]
# tomorrowHumidity = forecastJson["list"][1]["humidity"]
# tomorrowPressure = forecastJson["list"][1]["pressure"]
# tomorrowIcon = forecastJson["list"][1]["weather"][0]["icon"]
#
# tomorrowMsg = '{}°C   {}hPa   {}%\n'.format(tomorrowTemp,tomorrowPressure,tomorrowHumidity)
# t = pynotify.Notification('{}   -   {}'.format(city,tomorrow),tomorrowMsg,iconPath)

# day after tomorrow
# dayAfter = datetime.datetime.fromtimestamp(int(forecastJson["list"][2]["dt"])).strftime("%H:%M:%S %d.%m.%Y")
# dayAfterTemp = forecastJson["list"][2]["temp"]["day"]
# dayAfterHumidity = forecastJson["list"][2]["humidity"]
# dayAfterPressure = forecastJson["list"][1]["pressure"]
# dayAfterIcon = forecastJson["list"][2]["weather"][0]["icon"]
#
# dayAfterMsg = '{}°C   {}hPa   {}%\n'.format(dayAfterTemp,dayAfterPressure,dayAfterHumidity)
# d = pynotify.Notification('{}   -   {}'.format(city,dayAfter),dayAfterMsg,iconPath)
