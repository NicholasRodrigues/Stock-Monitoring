import requests
from twilio.rest import Client

STOCK_NAME = "PBR"
COMPANY_NAME = "Petrobras"

### You Have to get your won api keys and phone numbers for this to work


STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"


# Get yesterday's closing stock price.

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": stock_api_key,
}
response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = float(yesterday_data["4. close"])
print(yesterday_closing_price)

# Get the day before yesterday's closing stock price
before_yesterday_data = data_list[1]
before_yesterday_closing_price = float(before_yesterday_data["4. close"])
print(before_yesterday_closing_price)
# Find the positive difference between 1 and 2.
daily_variation = yesterday_closing_price - before_yesterday_closing_price
up_down = None
if daily_variation > 0:
    up_down = "📈"
else:
    up_down = "📉"

percentual_daily_variation = round((daily_variation/yesterday_closing_price) * 100)

if abs(percentual_daily_variation) > 5:
    news_params = {
       "apiKey": news_api_key,
        "qInTitle": COMPANY_NAME,
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]

    latest_articles = articles[:3]

    formatted_articles = [f"{STOCK_NAME}: {up_down}{percentual_daily_variation}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in latest_articles]

    client = Client(twilio_sid, twilio_auth_token)

    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_=twilio_phone_number,
            to=my_phone_number
        )


