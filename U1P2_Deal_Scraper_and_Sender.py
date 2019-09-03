#Overview: Checks if the lowest price available for a game, in this case Dark Souls III, is below a certain price. Sends SMS notification if it is.

#Library imports, API import
import requests
from bs4 import BeautifulSoup
from sinchsms import SinchSMS #API to send SMS
import time

URL = "https://isthereanydeal.com/game/darksoulsiii/info/"

headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}

#Price check def
#Uses BeautifulSoup to find the price and title, converts price to float
def price_check():
    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.content, 'lxml')

    global title 
    title = soup.find(id="gameTitle").get_text()
    global price 
    price = [float(p.get_text()[1:]) for p in soup.find_all(class_='gh-po__price')]

    global converted_price 
    converted_price = float(price[1])

    print(title)
    print(price)
    print(converted_price)

    if(converted_price < 20.0):
        send_sms()

#SMS send def. Sends sms to phone number using API if the price is below a certain price
def send_sms():

    title_id = str(title)
    price_value = str(converted_price)
    number = '+yournumber'
    message = title_id + " is available for $ " + price_value +  ", buy it now!"
    client = SinchSMS("appkey", "appsecret")

    print("Sending '%s' to %s" % (message, number))
    response = client.send_message(number, message)
    message_id = response['messageId']

    response = client.check_status(message_id)
    while response['status'] != 'Successful':
        print(response['status'])
        time.sleep(5)
        response = client.check_status(message_id)
        print(response['status'])

price_check()