import requests
from newsapi import NewsApiClient
import datetime as dt
import os
from twilio.rest import Client
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
today = dt.date.today() - dt.timedelta(days=3)
previous_day = dt.date.today() - dt.timedelta(days=4)
# print(today)
# print(previous_day)
output = []
## STEP 1: Use https://www.alphavantage.co

s_api = "87TSFJL95GPLW0E6"
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
stock_api = requests.get(url=f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={STOCK}&apikey={s_api}")
stock = stock_api.json()

today_market = stock["Time Series (Daily)"][str(today)]
p_day_market = stock["Time Series (Daily)"][str(previous_day)]
print(today_market)

t_high = float(today_market["2. high"])
p_high = float(p_day_market["2. high"])
t_low = float(today_market["3. low"])
p_low = float(p_day_market["3. low"])

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
# new_api = requests.get(url="")
if p_high*1.1 > t_high or p_high < t_high*1.1:
    n_api = "9d248049361e4167b5d35115cfa1ed67"
    newsapi = NewsApiClient(api_key=n_api)
    top_headlines = newsapi.get_top_headlines(q='bitcoin',
                                              category='business',
                                              country='us')
    sources = newsapi.get_sources()
    print(top_headlines['articles'][0])
    tot = len(top_headlines['articles'])

    for i in range(0, tot):
        output.append(top_headlines['articles'][i]['title'])
        output.append(top_headlines['articles'][i]["description"])

#
account_sid = 'ACf1a89f94435df65a63a0eb1dc7563516'
auth_token = 'ab3e36d1a1b8b270640645011bbe773f'
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body=f"{output}",
                     from_='+19199269381',
                     to='+919994448906'
                 )

print(message.sid)
print(output)

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 


#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

