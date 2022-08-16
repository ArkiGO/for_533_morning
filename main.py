from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
know_date = os.environ['KNOW_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp']), math.floor(weather['low']), math.floor(weather['high'])

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_know_count():
  delta = today - datetime.strptime(know_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)

current_date = today.strftime("%Y-%m-%d")
week_day = today.weekday();
if week_day == 0:
    current_date += " 星期一"
elif week_day == 1:
    current_date += " 星期二"
elif week_day == 2:
    current_date += " 星期三"
elif week_day == 3:
    current_date += " 星期四"
elif week_day == 4:
    current_date += " 星期五"
elif week_day == 5:
    current_date += " 星期六"
elif week_day == 6:
    current_date += " 星期日"
    
client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature, low_temperature, high_temperature = get_weather()
data = {
  "date":{"value": current_date},
  "weather":{"value":wea},
  "temperature":{"value":temperature},
  "low_temperature":{"value":low_temperature},
  "high_temperature":{"value":high_temperature},
  "love_days":{"value":get_count()},
  "know_days":{"value":get_know_count()},
  "birthday_left":{"value":get_birthday()},
  "words":{"value":get_words(), 
  "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
