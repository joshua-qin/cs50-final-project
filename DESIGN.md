# CS50 Final Project: Stocks.AI
## Design Report
### Joshua Qin and Claire Xu
#### Python Functions and .css File
###### app.py (functions specified below)
##### Plot:
This plot function utilizes the pyplot function of the matplotlib library, which is imported as plt in our program. The user-inputted ticker is obtained with request.form.get(“symbol”), from the plot.html file in which the user enters the desired ticker, and user errors are accounted for. We create a variable that holds that data path of the plot that is to be created; using a relative path to make our code more flexible and portable, we defined the base path of the file to be the working directory, which can be found with os.getcwd(), merged with the directory ‘static’, and we then add the filename as the name of the stock (ticker) and .png.
	Now that we have the path to the file of the specific stock’s plot, we first check if the desired plot has already been downloaded (meaning the user has already entered the same ticker into the plot function); if this is the case, then we simply return the template “plotted.html” with the ticker set to be the user-entered ticker. We’ll come back to this later.
	If the desired plot has not already been downloaded, we must download it. We use yfinance to download the stock data, then use the plot function to create a data plot, with respective axis values, and save the plot to the data path we specified earlier. We then again return the template “plotted.html” with the ticker set to be the user-entered ticker.
	In “plotted.html”, we utilize a JavaScript function to set the source path to be dependent on the ticker (since the plot of the specific ticker is saved as ticker.png). Essentially, we create an image variable and set its src attribute to the path of the plot file. Finally, we use img to actually display the obtained image of the plot.

##### Company News:
This function utilizes the API called NewsAPI, which scrapes news domains for news articles. Within this API, we used the function newsapi.get_everything(), which fetches all news articles within given parameters. We decided to limit the search with parameters ‘q’ (if a news article contains a phrase, which in this case is the user-inputted company name, obtained by request.form.get(“company”)), ‘from_param’ and ‘to’ (limits the time of publication of the news article), and ‘domains’ (limits the website domains that the function searches through).
While scraping through news articles, we attempt to find the most recent articles to ensure relevancy. To do this, we define a day_shift variable (which starts at 1), and change the from_param date with the day_shift variable. With a while loop beginning with a from_param date of yesterday’s date (‘to’ always remains at the current date), we see if we can find any articles. If so, we add it to our ‘urls’ list. If not, we increase the day_shift variable by 1 and continue to search for articles in the wider time frame.
Once we find articles in a certain time frame, we populate them into the ‘urls’ list. Each time the user requests a company name, we output a random website url in the ‘urls’ list. Through the HTML portion of our code, we embed this news article into our webpage using iframe.

##### Finance News:
This function largely follows the same outline as the Company News function. The only difference is, instead of having the user input a company they are interested in and searching for articles relevant to that company, we search for articles that include the keywords “finance” and “business”.

** For both Company News and Finance News, there are a few small logistical problems with the implementation of NewsAPI. The API requires a user key, which is associated with an account created with their website. However, each account only has 50 search credits per day, so we are unable to fetch more than 50 articles combined over Company News and Finance News in each 24 hour period. In addition, we embed the article urls that we find using the iframe element in HTML. However, many websites’ internal design does not allow external embedding. Therefore, our news sources are limited to only websites that we could embed through HTML.

##### Tips:
We created a .txt file with a list of investing tips, separated by row. We then read each row of the .txt file into a variable that holds a list of all the tips. Design-wise, storing the list in a .txt file makes it easier to modify the list of tips and add/remove tips. Finally, the random module is used to obtain a random tip from the list of tips, and this random tip is inputted through render_template(“tips.html, tip=tip). The tips.html file then displays the inputted random tip, and also contains a button that when clicked on, calls the tips() function once more to obtain another random tip.

##### Predict:
For this function, we credit the machine learning algorithm to: https://github.com/dataquestio/project-walkthroughs/blob/master/stock/StockProject.ipynb.

Since this function was based off of much of the work from the source above, in this design document, we will provide an overall overview of how the general machine learning algorithm works, and also provide insight on the design choices that were made in order to effectively implement the machine learning algorithm into our web application to achieve its desired functionality (allowing and utilizing user-entered input).

We will follow the code in the function from top to bottom. Enabling a user-inputted ticker for the stock they want to analyze, we use request.form.get to obtain the user-inputted ticker and handle possible error cases. To create a ticker-specific path (which will also be later used for the relevant file names to store the ticker’s stock data), we used os.path.join to concatenate different parts of the file path and enable our file path naming to be dynamic, being able to take on different tickers and create different file names with these tickers. Using this variable of the ticker’s path to the downloaded data, we first check if the path already exists, meaning the data for that ticker has already been downloaded, to save runtime and prevent downloading repetitive data. If the path does not exist, then we download the ticker’s data using yfinance.

Next, this is where the machine learning process begins. First, we set up the “target”, which is essentially a set of “accurate” values that the machine learning model will run and train on. The target is set up by taking the stock price history as real-world evidence of stock price trends that have actually occurred (corresponding to an “accurate” trend). To predict the stock price for tomorrow, we shift all the data by a day, allowing us to train our model on past data. The training data that the model runs on is from the ticker’s historical stock price data.

To train the model and generate predictions, we utilize a Random Forest Classifier, which is a general model commonly used in machine learning models due to its ability to landscape nonlinear relationships. In the for loop, the machine learning model is essentially trained over past data in increments, and the Random Forest Classifier is utilized to generate the predictions. Here is where the user-inputted confidence value becomes relevant. Through a set of inequalities, this confidence value serves as a threshold for generating the predictions; if the “score” of the prediction exceeds the threshold specified by the confidence value, then the value of the prediction is set to 1, and otherwise, it is kept at 0. Finally, this prediction value is related to the output message; if the value is 1, the message recommends investing in the stock, and if the value is 0, the message does not recommend investing in the stock.

##### Home
This function redirects the user to the homepage.html file. It also reads the list of quotes, and then uses the random module to choose a random quote from the list of quotes to display in the homepage.html file.

##### helpers.py
The only function in our helpers file is the apology function, which outputs a meme with apology text. This function was given to us in the finance problem set, and we thought it would be a cute (and necessary to handle errors) aspect to also implement in our own project. This apology function is in helpers.py because it is used through most of the functions, creating a clear distinction between main functions and this “helper function.”

style.css
In our style file, we define the style of four elements: the font family for the text throughout the website (monospace), the size of the font for the title (Stocks.AI), the color of the font for the title, and the size of any regular text in the website.


#### .html files

##### layout.html
This file is the foundational .html file that serves as a template for all the other .html files. We use bootstrap to create a navigation bar with items that are the different functions the program contains. We also implement a footer to credit the resources that helped us make this web application.

##### predict.html
This file is what appears when the user clicks on Predict in the navigation bar. It utilizes a form that allows a user to enter a stock ticker and choose a confidence value using a slider.

##### prediction.html
This file appears as a result of the Predict function and displays either a recommendation to invest in the stock or to not invest in the stock (using the result variable, which holds one of the two messages recommending either to invest or not invest).

##### plot.html:
The file is what appears when the user clicks on Plot. It utilizes a form that allows the user to enter a stock ticker and includes a button to submit.

##### plotted.html
This file appears as a result of the Plot function and displays the plot of the specific stock.

##### companynews.html
This file is what appears when the user clicks on Company News in the navigation bar. It utilizes a form that allows a user to enter the name of a company.

##### companyarticle.html
This file appears as a result of the Companynews function and displays a retrieved news article about the company using iframe. Since certain news outlets do not allow their websites to be used with iframe, we restricted the possible sources to only news outlets that allowed their webpages to be displayed with iframe.

##### financenews.html
This file appears as a result of clicking on Finance News and the Financenews function and displays a relevant finance news article using iframe.

##### tips.html
This file appears as a result of clicking on Tips (or clicking the button to show another tip), and displays a page with a random investing tip, along with a button that allows the user to generate another tip.

##### apology.html
This file is based off of the apology.html file used in the Finance pset (credits: CS50). To generate the apology image, the meme generator resource memegen.link is used, and an image link of the CS50 duck is inputted as the image source.

##### homepage.html
This file serves as the homepage. In addition to some welcome test, a random Warren Buffet quote from a list is displayed, and iframe was used to display Wall Street Journal’s finance big board.
