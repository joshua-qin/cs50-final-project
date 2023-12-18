# Project Title: Stocks.AI

## Project Description:
Stocks.AI is a comprehensive web application that provides first-time investors with guidance on the stock market. It includes various tools to guide investors, such as investing tips, graphs of past stock performance, articles relevant to specific companies and the financial market, and even a machine-learning model that generates suggestions on whether or not to invest in a stock. With Stocks.AI, investors can improve their knowledge of the stock market and make informed investment decisions!

## Youtube Demonstration:
https://youtu.be/UKZVkSZQcM0

## How to Install and Run the Program:
Make sure to install the following:
1. newsapi-python
2. yFinance
3. scikit-learn
4. datetime
5. pandas (which can be installed with yFinance)
6. matplotlib

In cs50.dev environment, change the working directory to the stocks folder, and then execute flask run in the terminal.

### Homepage:
The homepage displays a welcome message, a random motivational quote from Warren Buffet chosen from a pre-created list, and Wall Street Journal’s stock market big board.

### Predict:
Purpose: This function implements a machine learning model in order to forecast whether a specified stock’s price will rise or fall over the next day, given a certain confidence interval. If the machine learning model predicts that the stock’s price will rise, then the function will recommend the user to invest in that specific stock; if the machine learning model predicts that the stock’s price will not rise, then then the function will recommend the user to not invest in that specific stock. Keep in mind that each time the function is run, a machine learning model is being built and trained, so the function usually takes around 20-30 seconds.
Intput: Users submit two parameters via a form. The first parameter is the ticker of the stock of interest. Make sure that a valid ticker is entered, or else an error message will be displayed. The second parameter is the confidence interval, entered as a value with a slider, from 0 to 100. The higher the confidence interval, the higher the threshold that the machine learning model must overcome before making its prediction that the user should invest. As such, choosing a higher confidence interval essentially makes the machine learning model stricter in its predictions, and will make it less likely that the machine learning model recommends the user to invest. Choosing a confidence interval of 30-50 is recommended.
Output: The user is directed to a webpage that displays text recommending the user to invest, or to not invest, in the inputted stock.

### Plot:
Purpose: Given a user-inputted stock, this function outputs a graph displaying the entire stock price history of the specific stock.
Input: User submits one parameter via a form: the ticker of the stock of interest. Ensure that a valid ticker is entered, or else an error message will be displayed.
Output: The user is directed to a webpage that displays a graph that shows how the stock price of the inputted stock has changed over its entire lifetime on the stock market.

### Company News:
Purpose: This function outputs a relevant news article (within the past month, staying up to date as time passes) when given a user input of a company name. The article generated will be random, so a user can re-input the same company name and get a new article. The news article will be embedded in the webpage.
Input: Users enter a name of a company they are interested in. The capitalization of the name does not affect results.
Output: The user is directed to a webpage that displays an embed of a relevant news article about the company the user is interested in. If no relevant articles are found, the program will output an apology page.

### Finance News:
Purpose: This function outputs a relevant finance/business news article (within the past month, staying up to date as time passes). It does not take any user input. The article will be generated at random from a large subset of articles found, and users can reload the webpage to generate a new article.
Input: N/A
Output: The user is directed to a webpage that displays an embed of a relevant finance/business news article. If no relevant articles are found, the program will output an apology page.

**The webpage will have a rate limit of 50 articles generated (combined, for both finance news and company news) per 24-hour period.

### Tips:
Purpose: Provide the user with a random investing tip.
Input: N/A
Output: An investing tip, randomly chosen from a pre-created list of investing tips, is outputted. A button that allows users to choose another investing tip is also displayed.
