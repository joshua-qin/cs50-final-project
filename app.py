import os

from flask import Flask, render_template, request
from flask_session import Session
from newsapi import NewsApiClient
import random
from datetime import datetime, timedelta

from helpers import apology

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestClassifier


# Configure application
app = Flask(__name__, static_url_path = "/static", static_folder = "static")

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Reference: CS 50 Resources (Finance)
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def home():
    with open('quotes.txt', 'r') as file:
        quotes_list = file.readlines()

    # Choose a random quote from the list of quotes
    quote = random.choice(quotes_list)
    return render_template("homepage.html", quote=quote)

@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "POST":

        ticker = request.form.get("symbol")
        confidence = float(request.form.get("certainty")) / 100

        # Handle the error that a ticker is not entered
        if not ticker:
            return apology("Must enter a ticker.")

        # Create file path/name
        DATA_PATH = os.path.join(ticker + "_data.json")

        if os.path.exists(DATA_PATH):
            # Read from file if we've already downloaded the data.
            with open(DATA_PATH) as f:
                stock_hist = pd.read_json(f)
        else:
            # Get data
            stock = yf.Ticker(ticker)
            stock_hist = stock.history(period="max")

            # Handle exception for an invalid ticker
            if stock_hist.empty:
                return apology("Must enter a valid ticker.")

            # Save file to json in case we need it later.  This prevents us from having to re-download it every time.
            stock_hist.to_json(DATA_PATH)

        data = stock_hist[["Close"]]
        data = data.rename(columns = {'Close':'Actual_Close'})

        # Get our target data (actual historical data of stock rise/fall)
        data["Target"] = stock_hist.rolling(2).apply(lambda x: x.iloc[1] > x.iloc[0])["Close"]

        # Shift stock prices forward one day, so we're predicting tomorrow's stock prices from today's prices
        stock_prev = stock_hist.copy()
        stock_prev = stock_prev.shift(1)

        # Create our training data
        predictors = ["Close", "Volume", "Open", "High", "Low"]
        data = data.join(stock_prev[predictors]).iloc[1:]
        model = RandomForestClassifier(n_estimators=100, min_samples_split=200, random_state=1)

        step = 750

        # Loop through the data in increments of step
        for i in range(1000, data.shape[0], step):

            # Split the data into training sets and testing sets
            train = data.iloc[0:i].copy()
            test = data.iloc[i:(i+step)].copy()

            # Fit the random forest model
            model.fit(train[predictors], train["Target"])

            # Make predictions
            preds = model.predict_proba(test[predictors])[:,1]
            preds = pd.Series(preds, index=test.index)
            preds[preds > confidence] = 1
            preds[preds<=confidence] = 0

        # prediction is either 1 or 0, corresponding to rise/fall in stock price
        prediction = int(preds.iloc[-1])

        if prediction == 1:
            result = "You should invest in " + ticker + " stock."
        else:
            result = "You should not invest in " + ticker + " stock."

        print(result)
        return render_template("prediction.html", result=result)

    else:
        return render_template("predict.html")

@app.route("/plot", methods=["GET", "POST"])
def plot():
    if request.method == "POST":
        # Set the ticker
        ticker = request.form.get("symbol")
        # Handle the error that a ticker is not entered
        if not ticker:
            return apology("Must enter a ticker.")

        # Get path and name image file
        base_path = os.path.join(os.getcwd(), 'static')
        file_name = ticker + '.png'
        DATA_PATH = os.path.join(base_path, file_name)

        # If file exists, access existing file
        if os.path.exists(DATA_PATH):
            return render_template("plotted.html", ticker=ticker)
        else:

            # Get the data
            data = yf.download(ticker)
            # Check if the data is empty, suggesting that the user entered an invalid ticker
            if data.empty:
                return apology("Enter Valid Ticker.")

            # Plot the data
            else:
                data['Adj Close'].plot()
                plt.title('Stock Prices of ' + ticker + ' stock')
                plt.xlabel('Year')
                plt.ylabel('Stock price, in dollars per share')

                # save figure
                plt.savefig(DATA_PATH)
                plt.close()
                return render_template("plotted.html", ticker=ticker)
    else:
        return render_template("plot.html")

@app.route("/companynews", methods=["GET", "POST"])
def companyNews():
    if request.method == "POST":
        # Get the name of the company the user wants
        name = request.form.get("company")

        if not name:
            return apology("Must enter a company name.")

        newsapi = NewsApiClient(api_key='96332566af374610929af18f8032d881')
        urls = []

        # Get date and time (for range of news articles)
        date = datetime.today().strftime('%Y-%m-%d')
        today = datetime.today()
        day_shift = 1
        num_days_ago = today - timedelta(days=day_shift)
        date_prior = num_days_ago.strftime('%Y-%m-%d')

        # While loop until we find at least one article: We want the most recent news articles for relevancy
        while True:
            # Get news sources
            all_articles = newsapi.get_everything(
                q=name,
                domains="economist.com, ft.com, cbsnews.com, msnbc.com, wsj.com",
                from_param=date_prior,
                to=date,
            )

            # Add all urls found to a list
            for article in all_articles['articles']:
                urls.append(article['url'])

            # Continuing the while loop if we don't find any sources
            if len(urls) == 0:
                day_shift += 1
                num_days_ago = today - timedelta(days=day_shift)
                date_prior = num_days_ago.strftime('%Y-%m-%d')
                max_shift = 30
                if day_shift == max_shift:
                    return apology("No recent articles found. Please try another company.")
            else:
                break

        # Generate random url from our list
        url_len = len(urls)
        num = random.randrange(url_len)

        real_url = urls[num]

        # Output news article
        return render_template("companyarticle.html", url=real_url)

    else:
        return render_template("companynews.html")

@app.route("/financenews", methods=["GET"])
def financeNews():
    newsapi = NewsApiClient(api_key='96332566af374610929af18f8032d881')
    urls = []

    # Get date and time (for range of news articles)
    date = datetime.today().strftime('%Y-%m-%d')
    today = datetime.today()
    day_shift = 1
    num_days_ago = today - timedelta(days=day_shift)
    date_prior = num_days_ago.strftime('%Y-%m-%d')

    # While loop until we find at least one article: We want the most recent news articles for relevancy
    while True:
        # Get news sources
        all_articles = newsapi.get_everything(
            q="finance" or "business",
            domains="economist.com, ft.com, cbsnews.com, msnbc.com, wsj.com",
            from_param=date_prior,
            to=date,
        )

        # Add all urls found to a list
        for article in all_articles['articles']:
            urls.append(article['url'])

        # Continuing the while loop if we don't find any sources
        if len(urls) == 0:
            day_shift += 1
            num_days_ago = today - timedelta(days=day_shift)
            date_prior = num_days_ago.strftime('%Y-%m-%d')
            max_shift = 30
            if day_shift == max_shift:
                return apology("No recent articles found.")
        else:
            break

    # Generate random url from our list
    url_len = len(urls)
    num = random.randrange(url_len)

    real_url = urls[num]

    # Output news article
    return render_template("financenews.html", url=real_url)



@app.route("/tips", methods=["GET", "POST"])
def tips():
    with open('tips.txt', 'r') as file:
        tips_list = file.readlines()

    # Choose random tip from list of tips
    tip = random.choice(tips_list)
    return render_template("tips.html", tip=tip)


